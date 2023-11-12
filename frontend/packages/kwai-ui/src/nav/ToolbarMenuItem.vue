<script setup lang="ts">
import { computed } from 'vue';
import type { MenuItem } from '../types';

interface Props {
  tag?: string
  menuItem: MenuItem
}
const props = withDefaults(defineProps<Props>(), { tag: 'li' });

const linkTag = computed(() => props.menuItem.route ? 'router-link' : 'a');
const to = computed(() => props.menuItem.route ? 'to' : null);
const href = computed(() => props.menuItem.url ? 'href' : null);
const click = computed(() => props.menuItem.method ? 'click' : null);
</script>

<template>
  <component :is="tag">
    <component
      :is="linkTag"
      :[to]="menuItem.route"
      :[href]="menuItem.url"
      class="hover:cursor-pointer"
      @[click]="menuItem.method"
    >
      {{ menuItem.title }}
    </component>
  </component>
</template>

<style scoped>

</style>
