import {
  createIdentifierSchema,
  JsonApiDataSchema,
  JsonApiDocumentSchema,
  useHttpApi,
  useHttpPaginationApi,
} from '@kwai/api';
import type {
  Pagination,
  ResourceItems,
} from '@kwai/api';
import * as v from 'valibot';
import type { MaybeRef } from 'vue';
import {
  useMutation, useQuery, useQueryClient,
} from '@tanstack/vue-query';
import { unref } from 'vue';
import type { ApiError } from '@kwai/ui';
import type { DateType } from '@kwai/date';
import { createDateTimeFromUTC } from '@kwai/date';

export interface UserInvitation {
  id?: string
  email: string
  firstname: string
  lastname: string
  remark: string
  mailedAt?: DateType | null
  expiredAt?: DateType
  confirmedAt?: DateType | null
  revoked: boolean
}

const JsonApiUserInvitationIdentifierSchema = createIdentifierSchema('user_invitations');
const JsonApiUserAttributesSchema = v.object({
  email: v.string(),
  first_name: v.string(),
  last_name: v.string(),
  remark: v.string(),
  mailed_at: v.optional(v.nullable(v.string())),
  expired_at: v.optional(v.nullable(v.string())),
  confirmed_at: v.optional(v.nullable(v.string())),
  revoked: v.boolean(),
});
const JsonApiUserInvitationDataSchema = v.object({
  ...JsonApiUserInvitationIdentifierSchema.entries,
  ...JsonApiDataSchema.entries,
  attributes: JsonApiUserAttributesSchema,
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
        email: resource.attributes.email,
        firstname: resource.attributes.first_name,
        lastname: resource.attributes.last_name,
        remark: resource.attributes.remark,
        mailedAt: resource.attributes.mailed_at ? createDateTimeFromUTC(resource.attributes.mailed_at) : undefined,
        expiredAt: resource.attributes.expired_at ? createDateTimeFromUTC(resource.attributes.expired_at) : undefined,
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
type JsonApiUserInvitationDocType = v.InferInput<typeof JsonApiUserInvitationDocSchema>;

const getAllUserInvitations = ({ offset = 0, limit = 0 }: Pagination): Promise<ResourceItems<UserInvitation>> => {
  const api = useHttpPaginationApi({
    offset, limit,
  }).url('/v1/auth/users/invitations');

  return api
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
    .then((data): ResourceItems<UserInvitation> => {
      const result = v.safeParse(JsonApiUserInvitationDocSchema, data);
      if (result.success) {
        return result.output as ResourceItems<UserInvitation>;
      }
      const errorMessage = result.issues.map(issue => `${issue.path?.join('.')}: ${issue.message}`).join(', ');
      throw new Error(errorMessage);
    });
};

export const useUserInvitations = ({ offset = 0, limit = 0 }: {
  offset?: MaybeRef
  limit?: MaybeRef
} = {}) => useQuery<ResourceItems<UserInvitation>, ApiError | Error>({
  queryKey: [
    'admin/user_invitations',
    {
      offset,
      limit,
    },
  ],
  queryFn: () => getAllUserInvitations({
    offset: unref(offset), limit: unref(limit),
  }),
});

const mutateUserInvitation = (invitation: UserInvitation): Promise<UserInvitation> => {
  const payload: JsonApiUserInvitationDocType = {
    data: {
      id: invitation.id,
      type: 'user_invitations',
      attributes: {
        first_name: invitation.firstname,
        last_name: invitation.lastname,
        email: invitation.email,
        remark: invitation.remark,
        revoked: invitation.revoked,
      },
    },
  };
  if (invitation.id) { // Update
    return useHttpApi()
      .url(`/v1/auth/users/invitations/${invitation.id}`)
      .patch(payload)
      .json()
      .then((data) => {
        const result = v.safeParse(JsonApiUserInvitationDocSchema, data);
        if (result.success) {
          return result.output as UserInvitation;
        }
        const errorMessage = result.issues.map(issue => `${issue.path?.join('.')}: ${issue.message}`).join(', ');
        throw new Error(errorMessage);
      });
  }
  // Create
  return useHttpApi()
    .url('/v1/auth/users/invitations')
    .post(payload)
    .json((data) => {
      const result = v.safeParse(JsonApiUserInvitationDocSchema, data);
      if (result.success) {
        return result.output as UserInvitation;
      }
      const errorMessage = result.issues.map(issue => `${issue.path?.join('.')}: ${issue.message}`).join(', ');
      throw new Error(errorMessage);
    });
};

type OnSuccessCallback = () => void;
type OnSuccessAsyncCallback = () => Promise<void>;
interface MutationOptions {
  onSuccess?: OnSuccessCallback | OnSuccessAsyncCallback
}

export const useUserInvitationMutation = ({ onSuccess }: MutationOptions = {}) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: UserInvitation) => mutateUserInvitation(data),
    onSuccess: async(data: UserInvitation) => {
      queryClient.setQueryData(['admin/user_invitations', data.id], data);
      if (onSuccess) {
        if (onSuccess.constructor.name === 'AsyncFunction') {
          await onSuccess();
        } else {
          onSuccess();
        }
      }
    },
    onSettled: () => queryClient.invalidateQueries({
      queryKey: ['admin/user_invitations'],
      exact: true,
    }),
  });
};

const recreateUserInvitation = (uuid: string): Promise<UserInvitation> => {
  return useHttpApi()
    .url(`/v1/auth/users/invitations/${uuid}`)
    .post()
    .json((data) => {
      const result = v.safeParse(JsonApiUserInvitationDocSchema, data);
      if (result.success) {
        return result.output as UserInvitation;
      }
      const errorMessage = result.issues.map(issue => `${issue.path?.join('.')}: ${issue.message}`).join(', ');
      throw new Error(errorMessage);
    });
  ;
};

export const useRecreateUserInvitationMutation = ({ onSuccess }: MutationOptions = {}) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (uuid: MaybeRef<string>) => recreateUserInvitation(unref(uuid)),
    onSuccess: async(data: UserInvitation) => {
      queryClient.setQueryData(['admin/user_invitations', data.id], data);
      if (onSuccess) {
        if (onSuccess.constructor.name === 'AsyncFunction') {
          await onSuccess();
        } else {
          onSuccess();
        }
      }
    },
  });
};
