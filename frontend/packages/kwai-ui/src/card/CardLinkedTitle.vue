<template>
  <a
    :href="link"
    class="inline-block mb-2"
  >
    <h5>
      <slot />
    </h5>
  </a>
</template>

<script setup lang="ts">
defineProps<{
  link: string
}>();
</script>
