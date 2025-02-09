<script setup lang="ts">
import { CloseIcon } from '../icons';

defineProps({ canBeClosed: Boolean });

const emit = defineEmits(['close']);
const close = () => {
  emit('close');
};

defineOptions({ inheritAttrs: false });
</script>

<template>
  <Teleport to="body">
    <div
      id="notify"
      class="fixed bottom-0 left-0 w-full z-10"
      v-bind="$attrs"
    >
      <CloseIcon
        v-if="canBeClosed"
        class="w-4 h-4 absolute top-0 right-0 m-2 hover:cursor-pointer"
        @click="close"
      />
      <slot />
    </div>
  </Teleport>
</template>
