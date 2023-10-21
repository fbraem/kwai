<template>
  <div class="container mx-auto py-20">
    <SectionTitle class="text-center">
      <span v-if="newsItem">
        {{ newsItem.texts[0].title }}
      </span>
      <span v-else>
        Nieuws
      </span>
    </SectionTitle>
    <LoadingAlert v-if="isLoading">
      Even geduld, we laden momenteel het nieuwsbericht...
    </LoadingAlert>
    <ErrorAlert
      v-else-if="error"
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
          class="py-5"
          v-html="newsItem.texts[0].content"
        />
        <hr>
        <div class="text-xs text-gray-600 pt-5">
          Gepubliceerd op {{ publishDate }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useNewsItem } from '@root/composables/useNewsItem.ts';
import { LoadingAlert, ErrorAlert } from '@kwai/ui';
import { useQueryClient } from '@tanstack/vue-query';
import SectionTitle from '@root/components/SectionTitle.vue';
import IntroductionText from '@root/components/IntroductionText.vue';
import { computed } from 'vue';

interface NewsItemPageProperty {
  id: string
}
const props = defineProps<NewsItemPageProperty>();

const queryClient = useQueryClient();
const retry = () => {
  queryClient.invalidateQueries(['portal/news', props.id]);
};

const { isLoading, isFetching, isError, data: newsItem, error } = useNewsItem(props.id);

const publishDate = computed(() => {
  if (newsItem) {
    return newsItem.value.publishDate.format('DD-MM-YYYY HH:mm:ss');
  }
  return '';
});
</script>
