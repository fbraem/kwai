<script setup lang="ts">
import Alert from './Alert.vue';
import { InfoIcon } from '../icons';
</script>

<template>
  <Alert>
    <template #icon>
      <InfoIcon class="fill-blue-500 w-8 h-8 mr-2" />
    </template>
    <slot />
  </Alert>
</template>
