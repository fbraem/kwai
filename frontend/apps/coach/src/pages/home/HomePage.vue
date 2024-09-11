<script setup lang="ts">
import { ContainerSection, ContainerSectionTitle, ContainerSectionContent, Card, CardTitle, ListIcon } from '@kwai/ui';
import { useI18n } from 'vue-i18n';
import TrainingDefinitionsCard from '@root/pages/home/components/TrainingDefinitionsCard.vue';
const { t } = useI18n({ useScope: 'global' });
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>
      {{ t('home.description') }}
    </ContainerSectionTitle>
    <ContainerSectionContent>
      <TrainingDefinitionsCard />
      <Card class="w-full">
        <template #header>
          <CardTitle class="p-3 font-bold text-lg text-gray-900">
            {{ t('home.trainings.title') }}
          </CardTitle>
        </template>
        <p class="p-3">
          {{ t('home.trainings.description') }}
        </p>
        <template #footer>
          <div class="flex justify-between items-center p-3">
            <KwaiButton :to="{ name: 'coach.trainings' }">
              <ListIcon
                class="w-4 mr-2 fill-current"
              />
              {{ t('home.trainings.list') }}
            </KwaiButton>
          </div>
        </template>
      </Card>
    </containersectioncontent>
  </ContainerSection>
</template>

<style scoped>

</style>
