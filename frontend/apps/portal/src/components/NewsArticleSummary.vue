<template>
  <article
    :id="newsItem.id"
  >
    <h2 class="text-center text-3xl mb-6">
      {{ newsItem.texts[0].title }}
    </h2>
    <div
      class="leading-6 flex flex-col lg:flex-row gap-4 items-center"
    >
      <div class="w-32 flex-none">
        <div class="text-xs text-center uppercase font-semibold p-1.5 text-white bg-red-600 rounded-t">
          {{ newsItem.publish_date.format('MMMM') }}, {{ newsItem.publish_date.format('YYYY') }}
        </div>
        <div class="text-center text-6xl font-bold py-4">
          {{ newsItem.publish_date.format('D') }}
        </div>
      </div>
      <div
        class="mb-2.5 text-gray-700"
        v-html="newsItem.texts[0].summary"
      />
    </div>
  </article>
</template>

<script setup lang="ts">
import type { NewsItem } from '@root/stores/newsStore';

interface Props {
  newsItem: NewsItem
}

defineProps<Props>();
</script>
