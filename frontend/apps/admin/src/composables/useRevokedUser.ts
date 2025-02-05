import type { UserAccount } from '@root/composables/useUser.ts';
import { useMutation } from '@tanstack/vue-query';
import { useHttpApi } from '@kwai/api';


type OnSuccessCallback = () => void;
type OnSuccessAsyncCallback = () => Promise<void>;
interface MutationOptions {
  onSuccess?: OnSuccessCallback | OnSuccessAsyncCallback
}

const mutateRevokedUser = (user: UserAccount): Promise<void> => {
  const payload = {
    data: {
      id: user.id,
      type: 'revoked_users',
      attributes: { revoked: true },
    },
  };
  return useHttpApi()
    .url('/v1/auth/revoked_users')
    .post(payload)
    .json()
  ;
};

export const useRevokedUserMutation = ({ onSuccess }: MutationOptions = {}) => {
  return useMutation({
    mutationFn: (data: UserAccount) => mutateRevokedUser(data),
    onSuccess: async() => {
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

const mutateEnactUser = (user: UserAccount): Promise<void> => {
  const payload = {
    data: {
      id: user.id,
      type: 'revoked_users',
      attributes: { revoked: false },
    },
  };
  return useHttpApi()
    .url('/v1/auth/revoked_users')
    .post(payload)
    .json()
  ;
};

export const useEnactUserMutation = ({ onSuccess }: MutationOptions = {}) => {
  return useMutation({
    mutationFn: (data: UserAccount) => mutateEnactUser(data),
    onSuccess: async() => {
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
