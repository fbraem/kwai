<script setup lang="ts">
import Popover from 'primevue/popover';
import { ref } from 'vue';

const op = ref();
const toggle = (event: Event) => {
  op.value.toggle(event);
};
const show = () => {
  op.value.show();
};
const hide = () => {
  op.value.hide();
};
defineExpose({
  toggle,
  show,
  hide,
});
defineOptions({ inheritAttrs: false });
</script>

<template>
  <div>
    <Popover
      ref="op"
      :pt="{ content: () => 'p-0' }"
      v-bind="$attrs"
    >
      <div class="px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
        <div class="sm:flex sm:items-start">
          <div
            class="mx-auto flex size-12 shrink-0 items-center justify-center rounded-full sm:mx-0 sm:size-10"
          >
            <slot name="icon" />
          </div>
          <div class="text-center sm:text-left mt-3 sm:mt-0 sm:ml-4">
            <slot name="title" />
            <div class="mt-2">
              <slot />
            </div>
          </div>
        </div>
      </div>
      <slot name="footer" />
    </Popover>
  </div>
</template>
