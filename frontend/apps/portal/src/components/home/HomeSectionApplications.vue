<template>
  <section class="grid grid-cols-1 lg:grid-flow-col lg:auto-cols-fr">
    <ApplicationList :filter="applicationNames">
      <template
        v-for="(applicationName, index) in applicationNames"
        :key="applicationName"
        #[`app-${applicationName}`]="{ application }"
      >
        <router-link
          :to="{ name: `portal.${application.name}` }"
        >
          <div
            class="text-center text-white p-8 h-full"
            :class="{ 'bg-black' : index % 2, 'bg-red-600': !(index % 2) }"
          >
            <div class="rounded-full inline-flex items-center justify-center mb-3">
              <component
                :is="applications[application.name]"
                class="w-8 h-8 fill-white"
              />
            </div>
            <h2 class="text-2xl mb-2 font-medium">
              {{ application.title }}
            </h2>
            <p class="text-gray-200">
              {{ application.short_description }}
            </p>
          </div>
        </router-link>
      </template>
    </ApplicationList>
  </section>
</template>

<script setup lang="ts">
import ApplicationList from '@root/components/ApplicationList.vue';
import type { ShallowReactive } from 'vue';
import { computed } from 'vue';

interface ListedApplications {
  [key: string]: ShallowReactive<any>
}
interface ListedApplicationsProperty {
  applications: ListedApplications
}

const props = defineProps<ListedApplicationsProperty>();

const applicationNames = computed(() => Object.keys(props.applications));
</script>
