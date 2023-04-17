<template>
  <a
    :href="link"
    class="inline-block mb-2"
  >
    <h5>
      <slot></slot>
    </h5>
  </a>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

const props = defineProps<{
  link: string
}>()
</script>
