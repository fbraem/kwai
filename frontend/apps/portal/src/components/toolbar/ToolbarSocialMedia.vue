<template>
  <div class="flex flex-col md:flex-row place-content-between">
    <template
      v-for="socialMedia in portal.social_media"
      :key="socialMedia.title"
    >
      <a :href="socialMedia.url">
        <div class="flex items-center mb-2">
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
  </div>
</template>

<script setup lang="ts">
import { portal } from '@kwai/config';
import { defineAsyncComponent } from 'vue';

const loadIcon = (name: string) => {
  return defineAsyncComponent(() => import(`@root/components/icons/${name}.vue`));
};
</script>
