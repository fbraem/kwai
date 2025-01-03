<script setup lang="ts">
import Toolbar from 'primevue/toolbar';
import { useSlots } from 'vue';

interface Props {
  startClass?: string
  centerClass?: string
  endClass?: string
}

defineProps<Props>();
const slots = useSlots();

</script>

<template>
  <Toolbar
    :pt="{
      root: 'w-full',
      start: `flex-row ${startClass ?? 'self-start'}`,
      center: `flex-row ${centerClass ?? 'self-center'}`,
      end: `flex-row ${endClass ?? 'self-end'}`,
    }"
  >
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
