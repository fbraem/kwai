<script setup lang="ts">
import { useTrainingDefinitions } from '@root/composables/useTrainingDefinition';
import {
  ContainerSection,
  ContainerSectionBanner,
  ContainerSectionContent,
  ContainerSectionTitle,
  EditIcon,
  KwaiButton,
  NewIcon,
} from '@kwai/ui';
import { useI18n } from 'vue-i18n';
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
          <KwaiButton :to="{ name: 'coach.training_definitions.create' }">
            <NewIcon class="w-4 mr-2 fill-current" />
            {{ t('training_definitions.banner.button') }}
          </KwaiButton>
        </template>
      </containersectionbanner>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 w-full">
        <div
          v-for="trainingDefinition in trainingDefinitions"
          :key="trainingDefinition.id"
        >
          <TrainingDefinitionCard :training-definition="trainingDefinition">
            <template #footer>
              <div class="flex place-content-between">
                <KwaiButton
                  :to="{
                    name: 'coach.training_definitions.generate_trainings',
                    params: {
                      id: trainingDefinition.id
                    }
                  }"
                  small
                >
                  <AddCalendarIcon class="w-4 mr-2 fill-current" />
                  {{ t('training_definitions.card.buttons.generate') }}
                </KwaiButton>
                <KwaiButton
                  :to="{
                    name: 'coach.training_definitions.edit',
                    params: {
                      id: trainingDefinition.id
                    }
                  }"
                  small
                >
                  <EditIcon class="w-4 mr-2 fill-current " />
                  {{ t('training_definitions.card.buttons.edit') }}
                </KwaiButton>
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
