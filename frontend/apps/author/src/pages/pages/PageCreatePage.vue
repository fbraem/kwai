<script setup lang="ts">
import {
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
} from '@kwai/ui';
import { useI18n } from 'vue-i18n';
import { useApplications } from '@root/composables/useApplication';
import PageForm from '@root/pages/pages/components/PageForm.vue';

const { data: applications } = useApplications();

const { t } = useI18n({ useScope: 'global' });
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>{{ t('pages.create.title') }}</ContainerSectionTitle>
    <ContainerSectionContent>
      <PageForm :applications="applications" />
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
