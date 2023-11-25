<template>
  <router-link
    :to="to"
    class="inline-block mb-2"
  >
    <h5>
      <slot />
    </h5>
  </router-link>
</template>

<script setup lang="ts">
import { RouteLocationRaw } from 'vue-router';

defineProps<{
  to: RouteLocationRaw
}>();
</script>
