<template>
  <div class="mb-7 bg-white flex flex-col">
    <router-link
      class="flex items-end bg-cover"
      to="/news"
    >
      <NewsDate :date="newsItem.publishDate " />
      <div class="flex-grow p-2 border-b-2 border-red-600 items-center">
        <h3 class="text-xl text-gray-500 font-bold">
          <router-link to="/news">
            {{ newsItem.texts[0].title }}
          </router-link>
        </h3>
      </div>
    </router-link>
    <div class="p-6 bg-white flex flex-col">
      <p
        class="text-gray-500"
        v-html="newsItem.texts[0].summary"
      />
      <div class="mt-6 self-end">
        <router-link
          class="border border-red-600 bg-red-600 hover:bg-white hover:text-red-600 text-sm text-white py-1 px-3"
          :to="`/news/${newsItem.id}`"
        >
          Lees meer ...
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { NewsItem } from '@root/stores/newsStore';
import NewsDate from '@root/components/NewsDate.vue';

interface Props {
  newsItem: NewsItem
}

defineProps<Props>();
</script>
