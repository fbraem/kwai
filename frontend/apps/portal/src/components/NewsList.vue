<template>
  <NewsListModel v-slot="{ loading, newsItems }">
    <slot
      name="title"
      :loading="loading"
    />
    <template v-if="newsItems.length === 0">
      <slot name="empty" />
    </template>
    <template
      v-for="newsItem in newsItems"
      v-else
    >
      <slot :news-item="newsItem" />
    </template>
  </NewsListModel>
</template>

<script setup lang="ts">
import NewsListModel from './NewsListModel.vue';
</script>
