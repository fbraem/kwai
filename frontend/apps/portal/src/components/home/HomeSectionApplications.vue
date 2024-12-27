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
            class="flex flex-col text-center text-white p-8 h-full"
            :class="{ 'bg-black' : index % 2, 'bg-red-600': !(index % 2) }"
          >
            <div class="mb-3">
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
            <div class="flex-grow flex flex-col text-center items-center place-content-end">
              <LinkDownIcon class="w-4 h-4 fill-current" />
            </div>
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
import LinkDownIcon from '@root/components/icons/LinkDownIcon.vue';

interface ListedApplications {
  [key: string]: ShallowReactive<any>
}
interface ListedApplicationsProperty {
  applications: ListedApplications
}

const props = defineProps<ListedApplicationsProperty>();

const applicationNames = computed(() => Object.keys(props.applications));
</script>
