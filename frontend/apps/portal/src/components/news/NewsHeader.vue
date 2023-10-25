<template>
  <router-link
    class="flex items-end bg-cover"
    :to="`/news/${newsItem.id}`"
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
</template>

<script setup lang="ts">
import NewsDate from '@root/components/news/NewsDate.vue';
import type { NewsItem } from '@root/composables/useNewsItem.ts';

interface Props {
  newsItem: NewsItem
}

defineProps<Props>();
</script>

<style scoped>

</style>
