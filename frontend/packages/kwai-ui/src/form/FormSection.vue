<script setup lang="ts">
import FormSectionHeader from './FormSectionHeader.vue';

interface Props {
  title?: string
}
defineProps<Props>();
</script>
<template>
  <div class="md:grid md:grid-cols-3 md:gap-6">
    <div class="md:col-span-1">
      <slot name="title">
        <FormSectionHeader>
          {{ title }}
        </FormSectionHeader>
      </slot>
      <div class="text-gray-500 text-sm py-2">
        <slot name="description" />
      </div>
    </div>
    <div class="pt-5 md:pt-0 md:col-span-2">
      <slot />
    </div>
  </div>
</template>
