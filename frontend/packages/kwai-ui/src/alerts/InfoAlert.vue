<template>
  <Alert class="bg-blue-200 border-blue-600 mt-6">
    <template #icon>
      <InfoIcon class="fill-blue-600 w-8 h-8" />
    </template>
    <div class="text-sm text-blue-600">
      <slot />
    </div>
  </Alert>
</template>

<script setup lang="ts">
import Alert from './Alert.vue';
import InfoIcon from '../icons/InfoIcon.vue';
</script>
