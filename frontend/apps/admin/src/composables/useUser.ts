import {
  createIdentifierSchema,
  JsonApiDataSchema,
  JsonApiDocumentSchema,
  type ResourceItems,
  useHttpApi,
} from '@kwai/api';
import * as v from 'valibot';
import {
  createDateTimeFromUTC, type DateType,
} from '@kwai/date';
import type { MaybeRef } from 'vue';
import { unref } from 'vue';
import { useQuery } from '@tanstack/vue-query';

const JsonApiUserIdentifierSchema = createIdentifierSchema('user_accounts');
const JsonApiUserAttributesSchema = v.object({
  email: v.string(),
  last_login: v.nullable(v.string()),
  last_unsuccessful_login: v.nullable(v.string()),
  revoked: v.boolean(),
  admin: v.boolean(),
  first_name: v.string(),
  last_name: v.string(),
  remark: v.string(),
});

const JsonApiUserDataSchema = v.object({
  ...JsonApiUserIdentifierSchema.entries,
  ...JsonApiDataSchema.entries,
  attributes: JsonApiUserAttributesSchema,
});

type JsonApiUserType = v.InferInput<typeof JsonApiUserDataSchema>;

const JsonApiUserDocumentSchema = v.object({
  ...JsonApiDocumentSchema.entries,
  data: v.union([JsonApiUserDataSchema, v.array(JsonApiUserDataSchema)]),
});

export interface UserAccount {
  id: string
  email: string
  firstName: string
  lastName: string
  lastLogin: DateType | null
  lastUnsuccessfulLogin: DateType | null
  revoked: boolean
  admin: boolean
  remark: string
}

const getAllUsers = ({
  offset = 0,
  limit = 0,
}: {
  offset?: number
  limit?: number
}): Promise<ResourceItems<UserAccount>> => {
  let api = useHttpApi().url('/v1/auth/users');
  if (offset) {
    api = api.query({ 'page[offset]': offset });
  }
  if (limit) {
    api = api.query({ 'page[limit]': limit });
  }
  return api
    .get()
    .json()
    .then((data): ResourceItems<UserAccount> => {
      const result = v.safeParse(JsonApiUserDocumentSchema, data);
      if (result.success) {
        return {
          meta: result.output.meta!,
          items: (result.output.data as JsonApiUserType[]).map(user => ({
            id: user.id!,
            email: user.attributes.email,
            firstName: user.attributes.first_name,
            lastName: user.attributes.last_name,
            lastLogin: user.attributes.last_login
              ? createDateTimeFromUTC(user.attributes.last_login)
              : null,
            lastUnsuccessfulLogin: user.attributes.last_unsuccessful_login
              ? createDateTimeFromUTC(user.attributes.last_unsuccessful_login)
              : null,
            revoked: user.attributes.revoked,
            admin: user.attributes.admin,
            remark: user.attributes.remark,
          })),
        };
      }
      throw result.issues;
    });
};

export const useUsers = ({
  offset = 0,
  limit = 0,
}: {
  offset?: MaybeRef
  limit?: MaybeRef
} = {}) => {
  return useQuery({
    queryKey: [
      'admin',
      'users',
      {
        offset,
        limit,
      },
    ],
    queryFn: () =>
      getAllUsers({
        offset: unref(offset),
        limit: unref(limit),
      }),
  });
};
