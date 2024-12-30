<script setup lang="ts">
import {
  KwaiCard,
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
      <KwaiCard class="w-full">
        <template #title>
          Leden
        </template>
        Beheer de leden van jouw club.
        <template #footer>
          <div class="flex justify-between items-center">
            <KwaiButton
              :to="{ name: 'club.members' }"
              small
            >
              <ListIcon class="w-4 mr-2 fill-current" />
              Overzicht
            </KwaiButton>
            <KwaiButton
              :to="{ name: 'club.upload' }"
              small
            >
              <ListIcon class="w-4 mr-2 fill-current" />
              Upload
            </KwaiButton>
          </div>
        </template>
      </KwaiCard>
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
