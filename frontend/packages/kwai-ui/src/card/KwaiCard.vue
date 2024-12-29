<script setup lang="ts">
import Card from 'primevue/card';
import { useSlots } from 'vue';

const slots = useSlots();
</script>

<template>
  <Card>
    <template
      v-if="!!slots.title"
      #title
    >
      <slot name="title" />
    </template>
    <template
      v-if="!!slots.subtitle"
      #subtitle
    >
      <div class="text-sm">
        <slot name="subtitle" />
      </div>
    </template>
    <template
      v-if="!!slots.default"
      #content
    >
      <div class="p-5">
        <slot />
      </div>
    </template>
    <template
      v-if="!!slots.footer"
      #footer
    >
      <slot name="footer" />
    </template>
  </Card>
</template>

<style scoped>
</style>
