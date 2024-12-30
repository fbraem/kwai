<script setup lang="ts">
import {
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
  EditIcon,
  KwaiButton,
  KwaiCard,
} from '@kwai/ui';
import { useApplications } from '@root/composables/useApplication';
import PrimaryBadge from '@root/components/PrimaryBadge.vue';

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
                <PrimaryBadge
                  v-if="application.news"
                  class="bg-gray-200 text-gray-700"
                >
                  # News
                </PrimaryBadge>
                <PrimaryBadge
                  v-if="application.pages"
                  class="bg-gray-200 text-gray-700"
                >
                  # Pages
                </PrimaryBadge>
                <PrimaryBadge
                  v-if="application.events"
                  class="bg-gray-200 text-gray-700"
                >
                  # Events
                </PrimaryBadge>
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
