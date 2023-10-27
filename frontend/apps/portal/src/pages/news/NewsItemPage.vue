<template>
  <div
    v-if="newsItem"
    class="container mx-auto py-20"
  >
    <NewsHeader :news-item="newsItem" />
    <LoadingAlert v-if="isLoading">
      Even geduld, we laden momenteel het nieuwsbericht...
    </LoadingAlert>
    <ErrorAlert
      v-else-if="isError"
      class="max-w-lg mx-auto"
    >
      Oeps, er is iets fout gelopen...
      <a
        class="underline cursor-pointer"
        @click="retry"
      >
        Probeer opnieuw.
      </a>
    </ErrorAlert>
    <div
      v-else-if="newsItem"
      class="pt-5 xl:px-80"
    >
      <IntroductionText>
        <div v-html="newsItem.texts[0].summary" />
      </IntroductionText>
      <div
        v-if="newsItem.texts[0].content"
      >
        <hr>
        <div
          class="py-5 news-content"
          v-html="newsItem.texts[0].content"
        />
        <hr>
        <div class="text-xs text-gray-600 pt-5 flex place-content-between">
          <div>Gepubliceerd op {{ publishDate }}</div>
          <div>{{ newsItem.application.title }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useNewsItem } from '@root/composables/useNewsItem';
import { LoadingAlert, ErrorAlert } from '@kwai/ui';
import { useQueryClient } from '@tanstack/vue-query';
import IntroductionText from '@root/components/IntroductionText.vue';
import NewsHeader from '@root/components/news/NewsHeader.vue';
import { computed } from 'vue';

interface NewsItemPageProperty {
  id: string
}
const props = defineProps<NewsItemPageProperty>();

const queryClient = useQueryClient();
const retry = () => {
  queryClient.invalidateQueries({ queryKey: ['portal/news', props.id] });
};

const { isLoading, isError, data: newsItem } = useNewsItem(props.id);

const publishDate = computed(() => {
  if (newsItem.value) {
    return newsItem.value.publishDate.format('DD-MM-YYYY HH:mm:ss');
  }
  return '';
});
</script>

<style>
.news-content p {
    @apply py-3;
}
.news-content ul, .news-content ul > * {
  @apply list-disc list-inside;
}

.news-content h1 {
    @apply text-2xl font-bold mb-3;
}

.news-content h2 {
    @apply text-xl font-bold mb-3;
}

.news-content h3 {
    @apply text-lg font-bold  mb-3;
}

.news-content h4 {
    @apply font-bold mb-3;
}

.news-content a {
    @apply underline text-blue-500;
}

.news-content blockquote {
  @apply p-4 mb-4 border-l-4 bg-gray-200 border-gray-600;
}
</style>
