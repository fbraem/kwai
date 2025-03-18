<script setup lang="ts">
import EmailIcon from '@root/components/icons/EmailIcon.vue';
import MailedIcon from '@root/components/icons/MailedIcon.vue';
import type { UserInvitation } from '@root/composables/useUserInvitations';
import { computed } from 'vue';
import { now } from '@kwai/date';
import {
  DeleteIcon, KwaiButton,
} from '@kwai/ui';
import { useI18n } from 'vue-i18n';

interface Props {
  invitation: UserInvitation
}
const props = defineProps<Props>();

const emit = defineEmits(['renew', 'revoke']);

const expiredAt = computed(() => props.invitation.expiredAt!.format('L LTS'));
const isExpired = computed(() => {
  if (props.invitation.expiredAt) {
    return props.invitation.expiredAt.isBefore(now());
  }
  return false;
});
const mailedAt = computed(() => {
  if (props.invitation.mailedAt) {
    return props.invitation.mailedAt.format('L LTS');
  }
  return null;
});
const isMailSent = computed(() => {
  return props.invitation.mailedAt;
});
const confirmedAt = computed(() => {
  if (props.invitation.confirmedAt) {
    return props.invitation.confirmedAt.format('L LTS');
  }
  return null;
});

const renewInvitation = (event: Event) => {
  emit('renew', props.invitation, event);
};
const revokeInvitation = (event: Event) => {
  emit('revoke', props.invitation, event);
};

const { t } = useI18n({ useScope: 'global' });
</script>

<template>
  <div class="px-2 py-3 grid grid-cols-1 lg:grid-cols-4">
    <div class="flex flex-col">
      <div class="font-bold">
        {{ invitation.firstname }} {{ invitation.lastname }}
      </div>
      <div class="flex align-items-center">
        <div><EmailIcon class="w-4 mr-2" /></div>
        <div>{{ invitation.email }}</div>
      </div>
    </div>
    <div class="grid grid-cols-1 lg:col-span-2">
      <dl class="divide-y divide-surface-200 divide-dashed">
        <div class="lg:px-2 py-3 sm:grid sm:grid-cols-3 sm:gap-4">
          <dt class="text-sm font-medium text-gray-700">
            Expires at:
          </dt>
          <dd
            class="text-sm sm:col-span-2"
            :class="{'text-red-600': isExpired, 'font-medium': isExpired}"
          >
            {{ expiredAt }}
          </dd>
        </div>
        <div class="lg:px-2 py-3 sm:grid sm:grid-cols-3 sm:gap-4">
          <dt class="text-sm font-medium text-gray-700">
            Mailed at:
          </dt>
          <dd class="sm:col-span-2 flex flex-row items-center">
            <span class="text-sm">{{ mailedAt }}</span>
            <MailedIcon
              v-if="isMailSent"
              class="ml-2 fill-green-500"
            />
          </dd>
        </div>
        <div class="lg:px-2 py-3 sm:grid sm:grid-cols-3 sm:gap-4">
          <dt class="text-sm font-medium text-gray-700">
            Confirmed at:
          </dt>
          <dd class="text-sm sm:col-span-2">
            {{ confirmedAt }}
          </dd>
        </div>
      </dl>
    </div>
    <div class="grid place-content-end gap-2">
      <div>
        <KwaiButton
          small
          :method="(event: Event) => renewInvitation(event)"
          class="w-full"
        >
          <EmailIcon class="fill-current" />
          <span class="font-bold">
            {{ t('user_invitations.list.renew') }}
          </span>
        </KwaiButton>
      </div>
      <div>
        <KwaiButton
          small
          severity="danger"
          :method="(event: Event) => revokeInvitation(event)"
          class="w-full"
        >
          <DeleteIcon class="fill-white" />
          <span class="font-bold">
            {{ t('user_invitations.list.revoke') }}
          </span>
        </KwaiButton>
      </div>
    </div>
  </div>
</template>
