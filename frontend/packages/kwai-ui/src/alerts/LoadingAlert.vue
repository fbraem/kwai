<template>
  <Alert class="bg-gray-200 border-gray-600">
    <template #icon>
      <LoadingIcon class="fill-red-600 w-8 h-8" />
    </template>
    <slot />
  </Alert>
</template>

<script setup lang="ts">
import Alert from './Alert.vue';
import LoadingIcon from '../icons/LoadingIcon.vue';
</script>
