<script setup lang="ts">
withDefaults(
  defineProps<{
    bgDialog?: string
    bgInformation?: string
  }>(),
  {
    bgDialog: 'bg-white',
    bgInformation: 'bg-red-700',
  });
</script>

<template>
  <div
    class="flex flex-col sm:flex-row-reverse mb-6 shadow-lg rounded-lg max-w-6xl"
    :class="bgDialog"
  >
    <div
      class="w-full sm:w-1/2 md:w-1/3 sm:p-12 p-4 sm:rounded-r-lg"
      :class="bgInformation"
    >
      <slot name="information" />
    </div>
    <div class="flex flex-col w-full sm:w-1/2 md:w-2/3 pt-4 px-4 sm:px-12">
      <slot />
    </div>
  </div>
</template>
