<script setup lang="ts">
import NewsDate from '@root/components/news/NewsDate.vue';
import type { NewsItem } from '@root/composables/useNewsItem.ts';
import { KwaiTag } from '@kwai/ui';

interface Props {
  newsItem: NewsItem
}

defineProps<Props>();
</script>

<template>
  <router-link
    class="flex items-end bg-cover"
    :to="`/news/${newsItem.id}`"
  >
    <NewsDate :date="newsItem.publishDate " />
    <div class="flex-grow py-2 pl-2 border-b-2 border-red-600 items-center">
      <h3 class="flex content-between text-2xl text-gray-500 font-bold">
        <span class="inline-block flex-grow">
          {{ newsItem.texts[0].title }}
        </span>
        <router-link
          :to="`/news/application/${newsItem.application.name}`"
        >
          <div class="mr-2">
            <KwaiTag severity="secondary">
              {{ newsItem.application.title }}
            </KwaiTag>
          </div>
        </router-link>
      </h3>
    </div>
  </router-link>
</template>

<style scoped>

</style>
