<script setup lang="ts">
import KwaiAlert from './KwaiAlert.vue';
import { WarningIcon } from '../icons';
</script>

<template>
  <KwaiAlert severity="warn">
    <template #icon>
      <WarningIcon class="fill-orange-500 w-8 h-8 mr-2" />
    </template>
    <slot />
  </KwaiAlert>
</template>
