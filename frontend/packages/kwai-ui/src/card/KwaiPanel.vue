<script setup lang="ts">
import Panel from 'primevue/panel';
</script>

<template>
  <Panel>
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
