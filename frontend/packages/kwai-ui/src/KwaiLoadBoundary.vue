<script setup lang="ts">
import LoadingIcon from './icons/LoadingIcon.vue';

interface Props {
  loading: boolean
}

defineProps<Props>();
</script>

<template>
  <div
    v-if="loading"
    class="m-auto"
  >
    <LoadingIcon class="fill-red-500 w-8 h-8" />
  </div>
  <div v-else>
    <slot />
  </div>
</template>
