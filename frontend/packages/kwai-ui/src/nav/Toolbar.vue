<template>
  <div class="flex justify-between items-center py-4 px-6">
    <div class="flex items-center">
      <button
        class="focus:outline-none md:hidden"
        :class="fillColor"
        @click="isOpen = true"
      >
        <BarsIcon class="w-4 h-4" />
      </button>
      <slot name="left" />
    </div>
    <div>
      <slot />
    </div>
    <div>
      <slot name="right" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSidebar } from './useSidebar.js';
import BarsIcon from '../icons/BarsIcon.vue';

interface Props {
  fillColor: string
}

withDefaults(
  defineProps<Props>(),
  {
    fillColor: 'fill-black',
  }
);

const { isOpen } = useSidebar();
</script>
