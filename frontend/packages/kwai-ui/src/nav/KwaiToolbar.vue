<script setup lang="ts">
import Toolbar from 'primevue/toolbar';
import { useSlots } from 'vue';

const slots = useSlots();
</script>

<template>
  <Toolbar>
    <template
      v-if="!!slots.start"
      #start
    >
      <slot name="start" />
    </template>
    <template
      v-if="!!slots.center"
      #center
    >
      <slot name="center" />
    </template>
    <template
      v-if="!!slots.end"
      #end
    >
      <slot name="end" />
    </template>
  </Toolbar>
</template>

<style scoped>

</style>
