<script setup lang="ts">
import {
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
} from '@kwai/ui';
import TeamForm from '@root/pages/teams/components/TeamForm.vue';

import { useI18n } from 'vue-i18n';
const { t } = useI18n({ useScope: 'global' });
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>{{ t('team.create.title') }}</ContainerSectionTitle>
    <ContainerSectionContent>
      <TeamForm />
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
