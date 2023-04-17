<template>
  <div class="mb-7 flex flex-col">
    <router-link
      class="block flex items-end bg-cover"
      style="height: 200px;"
      :style="{ 'background-image': `url(${newsImage})` }"
      to="/news"
    >
      <div class="text-center p-2 bg-red-600 text-white min-w-fit">
        <span class="block font-bold text-xl">
          {{ story.publish_date.format('D') }}
        </span>
        <span class="block text-sm">
          {{ story.publish_date.format('MMM') }}
        </span>
        <span class="block text-sm">
          {{ story.publish_date.format('YYYY') }}
        </span>
      </div>
    </router-link>
    <div class="p-6 bg-white flex-1 grid auto-rows-min">
      <h3 class="text-xl mb-4">
        <router-link to="/news">
          {{ story.contents[0].title }}
        </router-link>
      </h3>
      <p
        class="text-gray-500 flex-grow"
        v-html="story.contents[0].summary"
      />
      <div class="mt-6">
        <router-link
          class="border border-red-600 bg-red-600 hover:bg-white hover:text-red-600 text-white rounded-full py-1.5 px-3"
          to="/news"
        >
          Lees meer
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// eslint-disable-next-line import/no-absolute-path
import newsImage from '/news.jpg';

import type { NewsStory } from '@root/stores/newsStore';

interface Props {
  story: NewsStory
}

defineProps<Props>();
</script>
