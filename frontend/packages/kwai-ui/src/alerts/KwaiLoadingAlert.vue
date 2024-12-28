<script setup lang="ts">
import KwaiAlert from './KwaiAlert.vue';
import LoadingIcon from '../icons/LoadingIcon.vue';
</script>

<template>
  <KwaiAlert>
    <template #icon>
      <LoadingIcon class="fill-blue-500 w-8 h-8 mr-2" />
    </template>
    <slot />
  </KwaiAlert>
</template>
