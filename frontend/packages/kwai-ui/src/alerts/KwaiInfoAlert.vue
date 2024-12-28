<script setup lang="ts">
import KwaiAlert from './KwaiAlert.vue';
import { InfoIcon } from '../icons';
</script>

<template>
  <KwaiAlert>
    <template #icon>
      <InfoIcon class="fill-blue-500 w-8 h-8 mr-2" />
    </template>
    <slot />
  </KwaiAlert>
</template>
