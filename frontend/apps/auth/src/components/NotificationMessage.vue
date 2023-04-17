<template>
  <Teleport to="#notify">
    <CloseIcon
      v-if="canBeClosed"
      class="w-4 h-4 absolute right-0 m-2 hover:cursor-pointer"
      @click="close"
    />
    <div class="bg-white p-10 text-center font-medium">
      <slot />
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { CloseIcon } from '@kwai/ui';
defineProps({
  canBeClosed: Boolean,
});
const emit = defineEmits(['close']);
const close = () => {
  emit('close');
};
</script>
