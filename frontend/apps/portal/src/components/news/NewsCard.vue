<script setup lang="ts">
import type { NewsItem } from '@root/composables/useNewsItem.ts';
import NewsHeader from '@root/components/news/NewsHeader.vue';
import { KwaiButton } from '@kwai/ui';

interface Props {
  newsItem: NewsItem
}

defineProps<Props>();
</script>
<template>
  <div class="mb-7 bg-white flex flex-col">
    <NewsHeader :news-item="newsItem" />
    <div class="p-6 bg-white flex flex-col">
      <p
        class="text-gray-500"
        v-html="newsItem.texts[0].summary"
      />
      <div class="mt-6 self-end">
        <KwaiButton
          small
          :to="{
            name: 'portal.news.item',
            params: {
              id: newsItem.id
            }
          }"
        >
          Lees meer...
        </KwaiButton>
      </div>
    </div>
  </div>
</template>
