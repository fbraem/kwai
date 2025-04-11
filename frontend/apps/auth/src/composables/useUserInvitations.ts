import * as v from 'valibot';
import {
  JsonApiDataSchema, JsonApiDocumentSchema, createIdentifierSchema,
  useHttpApi,
} from '@kwai/api';
import {
  createDateTimeFromUTC, type DateType,
} from '@kwai/date';
import {
  unref, type MaybeRef,
} from 'vue';
import { useQuery } from '@tanstack/vue-query';
import type { ApiError } from '@kwai/ui';

export interface UserInvitation {
  id: string
  expiredAt: DateType
  confirmedAt: DateType | null
  revoked: boolean
}

const JsonApiUserInvitationIdentifierSchema = createIdentifierSchema('user_invitations');
const JsonApiUserInvitationAttributesSchema = v.object({
  expired_at: v.string(),
  confirmed_at: v.optional(v.nullable(v.string())),
  revoked: v.boolean(),
});

const JsonApiUserInvitationDataSchema = v.object({
  ...JsonApiUserInvitationIdentifierSchema.entries,
  ...JsonApiDataSchema.entries,
  attributes: JsonApiUserInvitationAttributesSchema,
});
type JsonApiUserInvitationType = v.InferInput<typeof JsonApiUserInvitationDataSchema>;

const JsonApiUserInvitationDocSchema = v.pipe(
  v.object({
    ...JsonApiDocumentSchema.entries,
    data: v.union([JsonApiUserInvitationDataSchema, v.array(JsonApiUserInvitationDataSchema)]),
  }),
  v.transform((doc) => {
    const mapModel = (resource: JsonApiUserInvitationType): UserInvitation => {
      return {
        id: resource.id!,
        expiredAt: createDateTimeFromUTC(resource.attributes.expired_at),
        confirmedAt: resource.attributes.confirmed_at ? createDateTimeFromUTC(resource.attributes.confirmed_at) : null,
        revoked: resource.attributes.revoked,
      };
    };
    if (Array.isArray(doc.data)) {
      return {
        meta: {
          count: doc.meta?.count || 0,
          offset: doc.meta?.offset || 0,
          limit: doc.meta?.limit || 0,
        },
        items: doc.data.map(mapModel),
      };
    } else {
      return mapModel(doc.data);
    }
  })
);

const getUserInvitation = ({ id }: { id: string }): Promise<UserInvitation> => {
  return useHttpApi()
    .url(`/v1/auth/users/invitations/${id}`)
    .get()
    .json()
    .catch((error) => {
      if (error.response) {
        throw {
          status: error.response.status,
          message: error.json.detail,
          url: error.response.url,
        };
      }
      throw error;
    })
    .then((data) => {
      const result = v.safeParse(JsonApiUserInvitationDocSchema, data);
      if (result.success) {
        return result.output as UserInvitation;
      }
      const errorMessage = result.issues.map(issue => `${issue.path?.join('.')}: ${issue.message}`).join(', ');
      throw new Error(errorMessage);
    });
};

export const useUserInvitation = ({ id }: { id: MaybeRef }) => useQuery<UserInvitation, ApiError | Error>({
  queryKey: ['auth/user_invitations', id],
  queryFn: () => getUserInvitation({ id: unref(id) }),
});
