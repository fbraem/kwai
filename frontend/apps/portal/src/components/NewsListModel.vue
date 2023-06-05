<!-- A renderless component for loading news stories -->
<template>
  <slot :stories="stories" />
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useNewsStore } from '@root/stores/newsStore';

const store = useNewsStore();
store.load();

const stories = computed(() => store.items);
</script>
