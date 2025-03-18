<script setup lang="ts">
import type { ResourceItems } from '@kwai/api';
import {
  DeleteIcon,
  KwaiApiErrorBoundary,
  KwaiButton,
  KwaiCard,
  KwaiNotificationMessage,
  KwaiPopover,
} from '@kwai/ui';
import {
  useRecreateUserInvitationMutation, useUserInvitationMutation, type UserInvitation,
} from '@root/composables/useUserInvitations';
import UserInvitationRow from '@root/pages/users/components/UserInvitationRow.vue';
import MailIcon from '@root/components/icons/EmailIcon.vue';
import { ref } from 'vue';
import {
  Translation as i18n, useI18n,
} from 'vue-i18n';

interface Props {
  invitations: ResourceItems<UserInvitation>
}

defineProps<Props>();

const selectedInvitation = ref<UserInvitation | null>(null);

const renewPopover = ref();
const confirmRenew = (invitation: UserInvitation, event: Event) => {
  selectedInvitation.value = invitation;
  renewPopover.value.toggle(event);
};
const { mutate: recreateUserInvitation } = useRecreateUserInvitationMutation({
  onSuccess: () => {
    notificationKeyPath.value = 'user_invitations.list.renew_popover.notification';
    showNotification.value = true;
    setTimeout(() => {
      showNotification.value = false;
    }, 3000);
  },
});
const renew = () => {
  recreateUserInvitation(selectedInvitation.value!.id!);
  renewPopover.value.hide();
};

const revokePopover = ref();
const confirmRevoke = (invitation: UserInvitation, event: Event) => {
  selectedInvitation.value = invitation;
  revokePopover.value.toggle(event);
};
const { mutate: revokeUserInvitation, error: revokeError } = useUserInvitationMutation({
  onSuccess: () => {
    notificationKeyPath.value = 'user_invitations.list.revoke_popover.notification';
    showNotification.value = true;
    setTimeout(() => {
      showNotification.value = false;
    }, 3000);
  },
});
const revoke = () => {
  const invitation: UserInvitation = {
    ...selectedInvitation.value!, revoked: true,
  };
  revokeUserInvitation(invitation);
  revokePopover.value.hide();
};
const showNotification = ref(false);
const closeNotification = () => {
  showNotification.value = false;
};
const notificationKeyPath = ref<string>('');

const { t } = useI18n({ useScope: 'global' });
</script>

<template>
  <KwaiNotificationMessage
    v-if="showNotification"
    can-be-closed
    @close="closeNotification"
    class="bg-surface-100 text-center p-10"
  >
    <i18n
      :keypath="notificationKeyPath"
      tag="p"
      scope="global"
    >
      <template #name>
        <span class="font-bold">{{ selectedInvitation!.firstname }} {{ selectedInvitation!.lastname }}</span>
      </template>
    </i18n>
  </KwaiNotificationMessage>
  <KwaiApiErrorBoundary
    :error="revokeError"
    :email="$kwai.admin?.email"
  >
    <template #message>
      {{ t('user_invitations.list.revoke_popover.error') }}
    </template>
  </KwaiApiErrorBoundary>
  <KwaiCard class="w-full">
    <div class="grid grid-rows-1">
      <div
        v-for="invitation in invitations.items"
        :key="invitation.id!"
        class="odd:bg-surface-100"
      >
        <UserInvitationRow
          :invitation="invitation"
          @revoke="(invitation, event: Event) => confirmRevoke(invitation, event)"
          @renew="(invitation, event: Event) => confirmRenew(invitation, event)"
        />
      </div>
    </div>
  </KwaiCard>
  <KwaiPopover
    class="sm:max-w-sm"
    ref="renewPopover"
  >
    <template #title>
      <h3 class="font-semibold text-gray-900">
        {{ t('user_invitations.list.renew_popover.title') }}
      </h3>
    </template>
    <i18n
      keypath="user_invitations.list.renew_popover.message"
      tag="p"
      scope="global"
    >
      <template #name>
        <span class="font-bold">{{ selectedInvitation?.firstname }} {{ selectedInvitation?.lastname }}</span>
      </template>
      <template #email>
        <span class="font-bold">{{ selectedInvitation?.email }}</span>
      </template>
    </i18n>
    <template #footer>
      <div
        class="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6 sm:gap-2"
      >
        <KwaiButton
          small
          :method="() => renew()"
        >
          <MailIcon class="fill-current" />
          {{ t('user_invitations.list.renew') }}
        </KwaiButton>
      </div>
    </template>
  </KwaiPopover>
  <KwaiPopover
    class="sm:max-w-sm"
    ref="revokePopover"
  >
    <template #title>
      <h3 class="font-semibold text-gray-900">
        {{ t('user_invitations.list.revoke_popover.title') }}
      </h3>
    </template>
    <i18n
      keypath="user_invitations.list.revoke_popover.message"
      tag="p"
      scope="global"
    >
      <template #name>
        <span class="font-bold">{{ selectedInvitation?.firstname }} {{ selectedInvitation?.lastname }}</span>
      </template>
    </i18n>
    <template #footer>
      <div
        class="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6 sm:gap-2"
      >
        <KwaiButton
          small
          severity="danger"
          :method="() => revoke()"
        >
          <DeleteIcon class="fill-current" />
          {{ t('user_invitations.list.revoke') }}
        </KwaiButton>
      </div>
    </template>
  </KwaiPopover>
  <div>
    {{ invitations }}
  </div>
</template>
