<script setup lang="ts">
defineEmits(['click']);
</script>

<template>
  <a
    class="hover:cursor-pointer text-sm font-bold px-12 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1"
    tabindex="0"
    @click="$emit('click')"
  >
    <slot />
  </a>
</template>
