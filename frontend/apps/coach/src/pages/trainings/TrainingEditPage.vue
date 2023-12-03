<script setup lang="ts">
import { computed } from 'vue';
import {
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
} from '@kwai/ui';
import TrainingForm from '@root/pages/trainings/components/TrainingForm.vue';
import { useI18n } from 'vue-i18n';
import { useTraining } from '@root/composables/useTraining';
import { useTrainingDefinitions } from '@root/composables/useTrainingDefinition';

interface Props {
  id: string
}
const props = defineProps<Props>();
const id = computed(() => props.id);

const { data: trainingDefinitions } = useTrainingDefinitions();
const enabled = computed<boolean>(() => {
  return trainingDefinitions !== undefined;
});

const { data: training } = useTraining(id, { enabled });

const { t } = useI18n({ useScope: 'global' });
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>{{ t('training.edit.title') }}</ContainerSectionTitle>
    <ContainerSectionContent>
      <TrainingForm
        :training="training"
        :definitions="trainingDefinitions"
      />
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
