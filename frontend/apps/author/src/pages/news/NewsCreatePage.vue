<script setup lang="ts">
import {
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
} from '@kwai/ui';
import { useI18n } from 'vue-i18n';
import { useApplications } from '@root/composables/useApplication';
import NewsForm from '@root/pages/news/components/NewsForm.vue';

const { data: applications } = useApplications();

const { t } = useI18n({ useScope: 'global' });
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>{{ t('news.create.title') }}</ContainerSectionTitle>
    <ContainerSectionContent>
      <NewsForm :applications="applications" />
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
