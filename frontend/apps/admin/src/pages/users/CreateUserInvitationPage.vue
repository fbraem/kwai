<script setup lang="ts">
import {
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
} from '@kwai/ui';
import { useI18n } from 'vue-i18n';
import UserInvitationForm from '@root/pages/users/components/UserInvitationForm.vue';

const { t } = useI18n({ useScope: 'global' });
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>{{ t('user_invitations.create.title') }}</ContainerSectionTitle>
    <ContainerSectionContent>
      <UserInvitationForm />
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
