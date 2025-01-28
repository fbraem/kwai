<script setup lang="ts">
import Popover from 'primevue/popover';
import { ref } from 'vue';

const op = ref();
const toggle = (event: Event) => {
  console.log('toggle', event);
  op.value.toggle(event);
};
const show = (event: Event) => {
  console.log('show', event);
  op.value.show();
};
const hide = (event: Event) => {
  console.log('hide', event);
  op.value.hide();
};
defineExpose({
  toggle,
  show,
  hide,
});
</script>

<template>
  <div>
    <Popover
      ref="op"
      :pt="{ content: () => 'p-0' }"
    >
      <slot />
    </Popover>
  </div>
</template>
