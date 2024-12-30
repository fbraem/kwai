<script setup lang="ts">
import Card from 'primevue/card';
import { useSlots } from 'vue';

const slots = useSlots();
</script>

<template>
  <Card
    :pt="{
      caption: 'py-3 border-b border-gray-200',
      body: 'p-0',
      title: 'px-3',
      subtitle: 'px-3 text-sm',
      footer: 'p-3'
    }"
  >
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
      <slot name="subtitle" />
    </template>
    <template
      v-if="!!slots.default"
      #content
    >
      <div class="p-3">
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
