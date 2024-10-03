<script setup lang="ts">
import Panel from 'primevue/panel';

const preset = {
  root: () => ({
    class: 'border rounded-lg',
  }),
  header: () => ({
    class: ['border-0'],
  }),
  content: () => ({
    class: ['border-0'],
  }),
};
</script>

<template>
  <Panel
    :pt="preset"
    :pt-options="{ mergeSections: true, mergeProps: true }"
  >
    <template
      v-if="$slots.header"
      #header
    >
      <slot name="header" />
    </template>
    <template
      v-if="$slots.footer"
      #footer
    >
      <slot name="footer" />
    </template>
    <slot />
  </Panel>
</template>

<style scoped>

</style>
