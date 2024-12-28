<script setup lang="ts">
import Alert from './KwaiAlert.vue';
import { ErrorIcon } from '../icons';
</script>

<template>
  <Alert severity="error">
    <template #icon>
      <ErrorIcon class="fill-red-500 w-8 h-8 mr-2" />
    </template>
    <slot />
  </Alert>
</template>
