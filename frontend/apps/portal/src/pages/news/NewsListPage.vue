<script setup lang="ts">
import NewsList from '@root/components/news/NewsList.vue';
import NewsCard from '@root/components/news/NewsCard.vue';
</script>

<template>
  <div class="container mx-auto py-20 px-2">
    <h2 class="text-4xl font-medium text-center pb-12">
      Nieuwsoverzicht
    </h2>
    <NewsList>
      <template #default="{ newsItem }">
        <NewsCard :news-item="newsItem" />
      </template>
    </NewsList>
  </div>
</template>
