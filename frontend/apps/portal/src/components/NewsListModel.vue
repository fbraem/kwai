<!-- A renderless component for loading news stories -->
<template>
  <slot
    :loading="loading"
    :news-items="newsItems"
  />
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useNewsStore } from '@root/stores/newsStore';

const store = useNewsStore();
const { loading } = store.load();

const newsItems = computed(() => store.items);
</script>
