<template>
  <div class="mb-7 bg-white flex flex-col">
    <NewsHeader :news-item="newsItem" />
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
import type { NewsItem } from '@root/composables/useNewsItem.ts';
import NewsHeader from '@root/components/news/NewsHeader.vue';

interface Props {
  newsItem: NewsItem
}

defineProps<Props>();
</script>
