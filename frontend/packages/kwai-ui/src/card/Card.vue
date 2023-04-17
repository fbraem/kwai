<template>
  <div class="flex flex-col block rounded-lg border shadow-md">
    <header v-if="!!slots.header">
      <slot name="header" />
    </header>
    <div v-if="!!$slots.default" class="flex-grow">
      <slot />
    </div>
    <footer v-if="!!slots.footer">
      <slot name="footer" />
    </footer>
  </div>
</template>

<script setup lang="ts">
import { useSlots } from "vue"

const slots = useSlots()
</script>
