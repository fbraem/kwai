<script setup lang="ts">
import { Card, CardTitle, ContainerSection, ContainerSectionContent, ContainerSectionTitle, EditIcon } from '@kwai/ui';
import { useApplications } from '@root/composables/useApplication';
import PrimaryBadge from '@root/components/PrimaryBadge.vue';
import PrimaryButton from '@root/components/PrimaryButton.vue';

const { data: applications } = useApplications();
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>Applicaties</ContainerSectionTitle>
    <ContainerSectionContent>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card
          v-for="application in applications"
          :key="application.id"
        >
          <template #header>
            <CardTitle class="p-3 font-bold text-lg text-gray-900">
              {{ application.title }}
            </CardTitle>
            <p class="px-3 pb-3 text-sm text-gray-600">
              {{ application.short_description }}
            </p>
          </template>
          <div class="p-3">
            {{ application.description }}
          </div>
          <template #footer>
            <div class="flex justify-between items-center p-3">
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
                <PrimaryButton :route="{ name: 'author.applications.edit', params: { id: application.id } }">
                  <EditIcon class="w-4 mr-2" />Wijzig
                </PrimaryButton>
              </div>
            </div>
          </template>
        </Card>
      </div>
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
