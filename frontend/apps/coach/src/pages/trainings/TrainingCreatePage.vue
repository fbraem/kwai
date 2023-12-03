<script setup lang="ts">
import { computed } from 'vue';
import {
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
} from '@kwai/ui';
import TrainingForm from '@root/pages/trainings/components/TrainingForm.vue';
import { useI18n } from 'vue-i18n';
import { useTrainingDefinitions } from '@root/composables/useTrainingDefinition';

const { data: trainingDefinitions } = useTrainingDefinitions();

const { t } = useI18n({ useScope: 'global' });
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>{{ t('training.create.title') }}</ContainerSectionTitle>
    <ContainerSectionContent>
      <TrainingForm :definitions="trainingDefinitions" />
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
