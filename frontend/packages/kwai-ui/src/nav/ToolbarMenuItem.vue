<script setup lang="ts">
import LinkTag from './LinkTag.vue';
import type { MenuItem } from '../types';

interface Props {
  tag?: string
  menuItem: MenuItem
}
withDefaults(defineProps<Props>(), { tag: 'li' });
</script>

<template>
  <component :is="tag">
    <LinkTag
      :route="menuItem.route"
      :url="menuItem.url"
      :method="menuItem.method"
    >
      {{ menuItem.title }}
    </Linktag>
  </component>
</template>

<style scoped>

</style>
