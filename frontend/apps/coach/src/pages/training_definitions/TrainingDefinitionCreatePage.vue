<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { ContainerSection, ContainerSectionContent, ContainerSectionTitle } from '@kwai/ui';
import TrainingDefinitionForm from '@root/pages/training_definitions/components/TrainingDefinitionForm.vue';

const { t } = useI18n({ useScope: 'global' });
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>{{ t('training_definition.create.title') }}</ContainerSectionTitle>
    <ContainerSectionContent>
      <TrainingDefinitionForm />
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
