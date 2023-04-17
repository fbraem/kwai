<template>
  <article
    :id="story.id"
  >
    <h2 class="text-center text-3xl mb-6">
      {{ story.contents[0].title }}
    </h2>
    <div
      class="leading-6 flex flex-col lg:flex-row gap-4 items-center"
    >
      <div class="w-32 flex-none">
        <div class="text-xs text-center uppercase font-semibold p-1.5 text-white bg-red-600 rounded-t">
          {{ story.publish_date.format('MMMM') }}, {{ story.publish_date.format('YYYY') }}
        </div>
        <div class="text-center text-6xl font-bold py-4">
          {{ story.publish_date.format('D') }}
        </div>
      </div>
      <div
        class="mb-2.5 text-gray-700"
        v-html="story.contents[0].summary"
      />
    </div>
  </article>
</template>

<script setup lang="ts">
import type { NewsStory } from '@root/stores/newsStore';

interface Props {
  story: NewsStory
}

defineProps<Props>();
</script>
