<script setup lang="ts">
import { computed } from 'vue';
import { useTrainingDefinition } from '@root/composables/useTrainingDefinition';
import { useI18n } from 'vue-i18n';
import { ContainerSection, ContainerSectionContent, ContainerSectionTitle } from '@kwai/ui';
import TrainingDefinitionForm from '@root/pages/training_definitions/components/TrainingDefinitionForm.vue';

interface Props {
  id: string
}
const props = defineProps<Props>();
const id = computed(() => props.id);

const { data: trainingDefinition } = useTrainingDefinition(id);

const { t } = useI18n({ useScope: 'global' });
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>{{ t('training_definition.edit.title') }}</ContainerSectionTitle>
    <ContainerSectionContent>
      <TrainingDefinitionForm
        :definition="trainingDefinition"
      />
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
