<script setup lang="ts">
import Alert from './Alert.vue';
import LoadingIcon from '../icons/LoadingIcon.vue';
</script>

<template>
  <Alert>
    <template #icon>
      <LoadingIcon class="fill-blue-500 w-8 h-8 mr-2" />
    </template>
    <slot />
  </Alert>
</template>
