<script setup lang="ts">
import { BarsIcon } from '@kwai/ui';
import ToolbarMenuItem from './ToolbarMenuItem.vue';

import { ref } from 'vue';
import type { MenuItem } from '../types';

interface Props {
  itemClass?: string,
  menuItems: MenuItem[]
}
defineProps<Props>();

const open = ref(false);
const toggleMenu = () => {
  open.value = !open.value;
};

</script>

<template>
  <nav class="w-full lg:px-6 lg:mx-auto lg:max-w-6xl">
    <div
      v-bind="$attrs"
      class="px-4 py-3"
    >
      <div
        class="lg:hidden uppercase inline-flex items-center hover:cursor-pointer"
        @click="toggleMenu"
      >
        <BarsIcon class="w-4 fill-gray-300 mr-2" /> Menu
      </div>
      <div
        :class="{ 'hidden': !open }"
        class="w-full lg:block lg:w-auto"
      >
        <ul class="flex flex-col lg:flex-row lg:space-x-8 lg:mt-0">
          <ToolbarMenuItem
            v-for="(menuItem) in menuItems"
            :key="menuItem.title"
            :menu-item="menuItem"
            class="py-3"
            :class="itemClass"
          />
        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>

</style>
