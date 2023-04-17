<template>
  <NewsListModel v-slot="{ stories }">
    <template v-for="story in stories">
      <slot :story="story" />
    </template>
  </NewsListModel>
</template>

<script setup lang="ts">
import NewsListModel from './NewsListModel.vue';
</script>
