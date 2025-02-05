<script setup lang="ts">
import {
  type UserAccount, useUsers,
} from '@root/composables/useUser.ts';
import {
  Translation as i18n, useI18n,
} from 'vue-i18n';
import {
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
  KwaiButton,
  KwaiPanel,
  KwaiPopover,
  WarningIcon,
} from '@kwai/ui';
import RevokedIcon from '@root/components/icons/RevokedIcon.vue';
import { ref } from 'vue';
import { useEnactUserMutation, useRevokedUserMutation } from '@root/composables/useRevokedUser.ts';
import EnactIcon from '@root/components/icons/EnactIcon.vue';

const { t } = useI18n({ useScope: 'global' });

const { data: users } = useUsers();
const revokePopover = ref();

const confirmRevoke = (user: UserAccount, event?: Event) => {
  selectedUser.value = user;
  revokePopover.value.toggle(event);
};
const selectedUser = ref<UserAccount | null>(null);

const { mutate: mutateRevokeUser } = useRevokedUserMutation({
  onSuccess: () => {
    console.log(selectedUser.value);
  },
});
const revoke = () => {
  mutateRevokeUser(selectedUser.value!);
  revokePopover.value.hide();
};

const { mutate: mutateEnactUser } = useEnactUserMutation();
const enact = (user: UserAccount) => {
  mutateEnactUser(user);
};
</script>

<template>
  <KwaiPopover
    class="sm:max-w-sm"
    ref="revokePopover"
  >
    <template #icon>
      <WarningIcon class="size-6 fill-red-500" />
    </template>
    <template #title>
      <h3 class="font-semibold text-gray-900">
        {{ t('users.revoke_message_title') }}
      </h3>
    </template>
    <div class="text-sm text-gray-500">
      <i18n
        keypath="users.revoke_message"
        tag="p"
        scope="global"
      >
        <template #name>
          <span class="font-bold">{{ selectedUser?.firstName }} {{ selectedUser?.lastName }}</span>
        </template>
      </i18n>
      <p class="text-xs mt-3">
        {{ t('users.revoke_not_remove_message') }}
      </p>
    </div>
    <template #footer>
      <div
        class="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6 sm:gap-2"
      >
        <KwaiButton
          small
          severity="danger"
          class="font-bold w-full sm:w-auto mt-3 sm:mt-0"
          :method="() => revoke()"
        >
          {{ t('users.revoke') }}
        </KwaiButton>
        <KwaiButton
          small
          class="font-bold w-full sm:w-auto mt-3 sm:mt-0"
          severity="secondary"
          :method="() => revokePopover.hide()"
        >
          {{ t('users.cancel') }}
        </KwaiButton>
      </div>
    </template>
  </KwaiPopover>
  <ContainerSection>
    <ContainerSectionTitle>
      {{ t('users.title') }}
    </ContainerSectionTitle>
    <ContainerSectionContent>
      <template v-if="users">
        <KwaiPanel
          v-for="user in users.items"
          :key="user.id"
          toggleable
          header-class="bg-surface-100"
        >
          <template #header>
            <div class="font-bold">
              {{ user.email }}
            </div>
          </template>
          <div class="p-2">
            <div class="flex">
              <div class="grow">
                <div class="font-bold text-lg">
                  {{ user.firstName }} {{ user.lastName }}
                </div>
                <p class="text-sm text-gray-600">
                  {{ user.remark }}
                </p>
              </div>
              <div class="grid grid-rows-2 gap-2">
                <div>
                  <div class="font-bold">
                    {{ t('users.last_login') }}:
                  </div>
                  <div>
                    {{ user.lastLogin?.format('L LTS') }}
                  </div>
                </div>
                <div>
                  <div class="font-bold">
                    {{ t('users.last_unsuccessful_login') }}:
                  </div>
                  <div>
                    {{ user.lastUnsuccessfulLogin?.format('L LTS') ?? '-' }}
                  </div>
                </div>
              </div>
            </div>
          </div>
          <template #icons>
            <RevokedIcon
              v-if="user.revoked"
              class="w-4 fill-red-500"
            />
          </template>
          <template #footer>
            <div class="flex">
              <KwaiButton
                v-if="user.revoked"
                small
                :method="(event?: Event) => enact(user)"
              >
                <EnactIcon class="w-4 fill-current" />
                {{ t('users.enact') }}
              </KwaiButton>
              <KwaiButton
                v-else
                small
                severity="danger"
                :method="(event?: Event) => confirmRevoke(user, event)"
              >
                <RevokedIcon class="w-4 fill-current" />
                {{ t('users.revoke') }}
              </KwaiButton>
            </div>
          </template>
        </KwaiPanel>
      </template>
    </ContainerSectionContent>
  </ContainerSection>
</template>
