<script setup lang="ts">
import Menubar from 'primevue/menubar';
import { MenuItem } from '../types';
import { computed } from 'vue';

interface Props {
  items: MenuItem[]
}
const props = defineProps<Props>();

const menuItems = computed(() => {
  return props.items.map(item => ({
    label: item.title,
    command: item.method,
    route: item.route,
    disabled: item.disabled ?? false,
  }));
});
</script>

<template>
  <Menubar
    :model="menuItems"
    pt:root:class="bg-primary-500 text-primary-text w-full lg:px-6 lg:mx-auto lg:max-w-6xl"
    :pt-options="{ mergeSections: false, mergeProps: true }"
  />
</template>

<style>
li[data-pc-section="menuitem"] {
  @apply text-gray-700;
}
</style>
