<script setup lang="ts">
import Alert from './Alert.vue';
import { WarningIcon } from '../icons';
</script>

<template>
  <Alert severity="warn">
    <template #icon>
      <WarningIcon class="fill-orange-500 w-8 h-8 mr-2" />
    </template>
    <slot />
  </Alert>
</template>
