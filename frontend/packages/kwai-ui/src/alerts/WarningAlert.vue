<script setup lang="ts">
import Alert from './Alert.vue';
import WarningIcon from '../icons/WarningIcon.vue';
</script>

<template>
  <Alert class="bg-orange-100 border-orange-500 mt-6">
    <template #icon>
      <WarningIcon class="fill-orange-500 w-8 h-8" />
    </template>
    <div class="text-sm text-orange-500">
      <slot />
    </div>
  </Alert>
</template>
