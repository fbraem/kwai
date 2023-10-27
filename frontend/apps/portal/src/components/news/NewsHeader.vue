<template>
  <router-link
    class="flex items-end bg-cover"
    :to="`/news/${newsItem.id}`"
  >
    <NewsDate :date="newsItem.publishDate " />
    <div class="flex-grow flex py-2 pl-2 border-b-2 border-red-600 items-center">
      <h3 class="flex-grow text-2xl text-gray-500 font-bold">
        {{ newsItem.texts[0].title }}
      </h3>
      <router-link
        :to="`/news/application/${newsItem.application.name}`"
      >
        <div>
          <span class="inline-block font-bold text-xs bg-gray-200 px-[0.65em] pb-[0.25em] pt-[0.35em]">
            {{ newsItem.application.title }}
          </span>
        </div>
      </router-link>
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
