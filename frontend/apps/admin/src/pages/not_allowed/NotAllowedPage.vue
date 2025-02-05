<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import {
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
} from '@kwai/ui';

const { t } = useI18n({ useScope: 'global' });

</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>{{ t('not_allowed.title') }}</ContainerSectionTitle>
    <ContainerSectionContent>
      <p>{{ t('not_allowed.description') }}</p>
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
