<script setup lang="ts">
import NewsList from '@root/components/news/NewsList.vue';
import NewsCard from '@root/components/news/NewsCard.vue';
import { useApplications } from '@root/composables/useApplication';
import { computed } from 'vue';

interface Props {
  application?: string
}
const props = defineProps<Props>();

const { data: applications } = useApplications();

const application = computed(() => {
  if (applications.value && props.application) {
    return applications.value.find(application => application.name === props.application);
  }
  return null;
});

</script>

<template>
  <div class="container mx-auto py-20 px-2">
    <div
      v-if="application"
      class="text-center pb-12"
    >
      <h2 class="text-4xl font-medium text-center">
        Nieuws: {{ application.title }}
      </h2>
      <router-link
        to="/news"
        class="text-sm underline text-blue-400"
      >
        Terug naar het overzicht
      </router-link>
    </div>
    <NewsList :application="props.application">
      <template #default="{ newsItem }">
        <NewsCard :news-item="newsItem" />
      </template>
    </NewsList>
  </div>
</template>
