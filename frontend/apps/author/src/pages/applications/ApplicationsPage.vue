<script setup lang="ts">
import {
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
  EditIcon,
  KwaiButton,
  KwaiCard,
  KwaiTag,
} from '@kwai/ui';
import { useApplications } from '@root/composables/useApplication';

const { data: applications } = useApplications();
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>Applicaties</ContainerSectionTitle>
    <ContainerSectionContent>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <KwaiCard
          v-for="application in applications"
          :key="application.id as string"
        >
          <template #title>
            {{ application.title }}
          </template>
          <template #subtitle>
            {{ application.short_description }}
          </template>
          {{ application.description }}
          <template #footer>
            <div class="flex justify-between items-center">
              <div class="flex space-x-2">
                <KwaiTag
                  v-if="application.news"
                  severity="secondary"
                >
                  # News
                </KwaiTag>
                <KwaiTag
                  v-if="application.pages"
                  severity="secondary"
                >
                  # Pages
                </KwaiTag>
                <KwaiTag
                  v-if="application.events"
                  severity="secondary"
                >
                  # Events
                </KwaiTag>
              </div>
              <div>
                <KwaiButton
                  :to="{ name: 'author.applications.edit', params: { id: application.id } }"
                  small
                >
                  <EditIcon class="w-4 mr-2 fill-current" />Wijzig
                </KwaiButton>
              </div>
            </div>
          </template>
        </KwaiCard>
      </div>
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
