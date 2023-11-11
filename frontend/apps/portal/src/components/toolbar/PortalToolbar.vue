<template>
  <header class="container mx-auto p-8 lg:px-6 lg:max-w-6xl">
    <div class="grid grid-flow-row lg:grid-flow-col space-y-4 items-center">
      <ToolbarLogo
        :url="website.url"
        :logo="logoUrl"
      >
        {{ website.title }}
      </ToolbarLogo>
      <div class="flex flex-col md:flex-row md:items-center">
        <ToolbarSocialMedia class="md:w-2/3" />
        <ToolbarUser class="md:w-1/3" />
      </div>
    </div>
  </header>
  <nav class="w-full lg:px-6 lg:mx-auto lg:max-w-6xl">
    <div class="bg-red-600 px-4 py-3">
      <div
        class="lg:hidden text-gray-300 uppercase inline-flex items-center hover:cursor-pointer"
        @click="toggleMenu"
      >
        <BarsIcon class="w-4 fill-gray-300 mr-2" /> Menu
      </div>
      <div
        :class="{ 'hidden': !open }"
        class="w-full lg:block lg:w-auto"
      >
        <ul class="text-gray-200 flex flex-col lg:flex-row lg:space-x-8 lg:mt-0">
          <li class="py-3 hover:text-white">
            <a :href="website.url">Home</a>
          </li>
          <ApplicationList>
            <template #default="{ application }">
              <li
                v-if="$router.hasRoute(`portal.${application.name}`)"
                class="py-3 hover:text-white"
              >
                <router-link :to="{ name: `portal.${application.name}` }">
                  {{ application.title }}
                </router-link>
              </li>
            </template>
          </ApplicationList>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
// eslint-disable-next-line import/no-absolute-path
import logoUrl from '/logo.png';

import { ToolbarLogo, BarsIcon } from '@kwai/ui';
import { website } from '@kwai/config';
import ApplicationList from '../ApplicationList.vue';
import { ref } from 'vue';
import ToolbarSocialMedia from './ToolbarSocialMedia.vue';
import ToolbarUser from './ToolbarUser.vue';

const open = ref(false);
const toggleMenu = () => {
  open.value = !open.value;
};
</script>
