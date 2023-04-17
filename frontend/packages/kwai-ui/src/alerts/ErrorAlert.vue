<template>
  <Alert class="bg-red-200 border-red-600 mt-6">
    <template #icon>
      <ErrorIcon class="fill-red-600 w-8 h-8" />
    </template>
    <div class="text-sm text-red-600">
      <slot />
    </div>
  </Alert>
</template>

<script setup lang="ts">
import Alert from './Alert.vue'
import ErrorIcon from "../icons/ErrorIcon.vue"
</script>
