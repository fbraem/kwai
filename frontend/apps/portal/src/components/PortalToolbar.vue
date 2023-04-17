<template>
  <header class="container mx-auto px-4">
    <div class="grid md:grid-cols-3 lg:grid-cols-4 items-center items-stretch py-4">
      <div class="md:col-span-3 lg:col-span-1 py-4">
        <a :href="website.url">
          <div class="flex flex-row items-center">
            <img
              :src="logoUrl"
              class="w-16 mr-4"
              alt="logo"
            >
            <div class="text-xl font-medium uppercase text-center">
              {{ website.title }}
            </div>
          </div>
        </a>
      </div>
      <template
        v-for="socialMedia in portal.social_media"
        :key="socialMedia.title"
      >
        <a :href="socialMedia.url">
          <div class="md:py-4 flex items-center mb-2">
            <div>
              <component
                :is="loadIcon(socialMedia.icon)"
                class="w-8 fill-red-600"
              />
            </div>
            <div class="flex flex-col pl-4">
              <h2 class="font-semibold">
                {{ socialMedia.title }}
              </h2>
              <span class="text-gray-600">
                {{ socialMedia.account }}
              </span>
            </div>
          </div>
        </a>
      </template>
      <div class="md:py-4 justify-self-end">
        <a
          href="http://localhost/auth/#login"
          class="px-3 py-2 flex items-center bg-red-600 text-white hover:bg-white hover:text-red-600 hover:cursor-pointer border border-red-600"
        >
          Login
        </a>
      </div>
    </div>
  </header>
  <nav>
    <div class="lg:max-w-5xl mx-auto bg-red-600 px-8 py-6">
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

import { BarsIcon } from '@kwai/ui';
import { website, portal } from '@kwai/config';
import ApplicationList from './ApplicationList.vue';
import { defineAsyncComponent, ref } from 'vue';

const open = ref(false);
const toggleMenu = () => {
  open.value = !open.value;
};

const loadIcon = (name: string) => {
  return defineAsyncComponent(() => import(`@root/components/icons/${name}.vue`));
};
</script>
