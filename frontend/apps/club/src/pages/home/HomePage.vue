<script setup lang="ts">
import {
  Card,
  CardTitle,
  ContainerSection,
  ContainerSectionTitle,
  ContainerSectionContent,
  KwaiButton,
  ListIcon,
} from '@kwai/ui';
import { useI18n } from 'vue-i18n';
const { t } = useI18n({ useScope: 'global' });
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>
      {{ t('home.description') }}
    </ContainerSectionTitle>
    <ContainerSectionContent>
      <Card class="w-full">
        <template #header>
          <CardTitle class="p-3 font-bold text-lg text-gray-900">
            Leden
          </CardTitle>
        </template>
        <p class="p-3">
          Beheer de leden van jouw club.
        </p>
        <template #footer>
          <div class="flex justify-between items-center p-3">
            <KwaiButton :to="{ name: 'club.members' }">
              <ListIcon
                class="w-4 mr-2 fill-current"
              />
              Overzicht
            </KwaiButton>
            <KwaiButton :to="{ name: 'club.upload' }">
              <ListIcon
                class="w-4 mr-2 fill-current"
              />
              Upload
            </KwaiButton>
          </div>
        </template>
      </Card>
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
