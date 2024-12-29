<script setup lang="ts">
import { ContainerSection, ContainerSectionTitle, ContainerSectionContent } from '@kwai/ui';
import { useI18n } from 'vue-i18n';
import TrainingDefinitionsCard from './components/TrainingDefinitionsCard.vue';
import TrainingsCard from './components/TrainingsCard.vue';
const { t } = useI18n({ useScope: 'global' });
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>
      {{ t('home.description') }}
    </ContainerSectionTitle>
    <ContainerSectionContent>
      <TrainingDefinitionsCard />
      <TrainingsCard />
    </containersectioncontent>
  </ContainerSection>
</template>

<style scoped>

</style>
