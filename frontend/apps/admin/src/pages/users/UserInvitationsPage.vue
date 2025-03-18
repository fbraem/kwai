<script setup lang="ts">
import { useUserInvitations } from '@root/composables/useUserInvitations.ts';
import {
  ContainerSection,
  ContainerSectionTitle,
  ContainerSectionContent,
  KwaiApiErrorBoundary,
  KwaiInfoAlert,
  KwaiButton,
  KwaiToolbar,
  NewIcon,
} from '@kwai/ui';
import { useI18n } from 'vue-i18n';
import UserInvitationList from '@root/pages/users/components/UserInvitationList.vue';

const { t } = useI18n({ useScope: 'global' });

const { data: userInvitations, error } = useUserInvitations();
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>User Invitations</ContainerSectionTitle>
    <ContainerSectionContent>
      <KwaiToolbar
        start-class="w-full sm:w-1/2"
        end-class="w-full sm:w-1/3 sm:place-content-end"
      >
        <template #start>
          <div class="flex flex-col">
            <h5 class="mr-3 font-semibold">
              {{ t('user_invitations.toolbar.title') }}
            </h5>
            <p class="text-gray-500">
              {{ t('user_invitations.toolbar.description') }}
            </p>
          </div>
        </template>
        <template #end>
          <KwaiButton
            :to="{ name: 'admin.user_invitations.create' }"
            small
          >
            <NewIcon class="w-4 mr-2 fill-current" />
            {{ t('user_invitations.toolbar.button') }}
          </KwaiButton>
        </template>
      </KwaiToolbar>
      <KwaiApiErrorBoundary
        :error="error"
        :email="$kwai.admin?.email"
      >
        <template #message>
          An error occurred while retrieving the user invitations.
        </template>
        <template v-if="userInvitations">
          <div v-if="userInvitations.meta.count === 0">
            <KwaiInfoAlert>There are no user invitations.</KwaiInfoAlert>
          </div>
          <UserInvitationList :invitations="userInvitations" />
        </template>
      </KwaiApiErrorBoundary>
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
