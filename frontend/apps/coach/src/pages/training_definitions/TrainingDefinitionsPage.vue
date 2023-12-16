<script setup lang="ts">
import { useTrainingDefinitions } from '@root/composables/useTrainingDefinition';
import {
  ContainerSection,
  ContainerSectionBanner,
  ContainerSectionContent,
  ContainerSectionTitle, EditIcon,
  NewIcon,
} from '@kwai/ui';
import { useI18n } from 'vue-i18n';
import PrimaryButton from '@root/components/PrimaryButton.vue';
import TrainingDefinitionCard from '@root/pages/training_definitions/components/TrainingDefinitionCard.vue';
import AddCalendarIcon from '@root/components/icons/AddCalendarIcon.vue';

const { t } = useI18n({ useScope: 'global' });

const { data: trainingDefinitions } = useTrainingDefinitions();
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>
      {{ t('training_definitions.title') }}
    </ContainerSectionTitle>
    <ContainerSectionContent>
      <ContainerSectionBanner>
        <template #left>
          <h5 class="mr-3 font-semibold">
            {{ t('training_definitions.banner.title') }}
          </h5>
          <p class="text-gray-500">
            {{ t('training_definitions.banner.description') }}
          </p>
        </template>
        <template #right>
          <PrimaryButton
            :route="{ name: 'coach.training_definitions.create' }"
            class="flex items-center"
          >
            <NewIcon class="w-4 mr-2 fill-current" />
            {{ t('training_definitions.banner.button') }}
          </PrimaryButton>
        </template>
      </containersectionbanner>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div
          v-for="trainingDefinition in trainingDefinitions"
          :key="trainingDefinition.id"
        >
          <TrainingDefinitionCard :training-definition="trainingDefinition">
            <template #footer>
              <div class="p-3 flex place-content-between">
                <PrimaryButton
                  class="inline-flex items-center"
                  :route="{
                    name: 'coach.training_definitions.generate_trainings',
                    params: {
                      id: trainingDefinition.id
                    }
                  }"
                >
                  <AddCalendarIcon class="w-4 mr-2 fill-current" />
                  {{ t('training_definitions.card.buttons.generate') }}
                </PrimaryButton>
                <PrimaryButton
                  class="inline-flex items-center"
                  :route="{
                    name: 'coach.training_definitions.edit',
                    params: {
                      id: trainingDefinition.id
                    }
                  }"
                >
                  <EditIcon class="w-4 mr-2 fill-current " />
                  {{ t('training_definitions.card.buttons.edit') }}
                </PrimaryButton>
              </div>
            </template>
          </TrainingDefinitionCard>
        </div>
      </div>
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
