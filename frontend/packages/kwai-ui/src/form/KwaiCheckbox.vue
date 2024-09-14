<script setup lang="ts">
import Checkbox from 'primevue/checkbox';

const model = defineModel<boolean>();

defineOptions({
  inheritAttrs: false,
});

const preset = {
  root: () => ({
    class: [
    ],
  }),
  // @ts-ignore
  box: ({ context }) => ({
    class: [
      { 'bg-primary-500': context.checked },
    ],
  }),
};
</script>

<template>
  <div class="flex items-center">
    <Checkbox
      v-model="model"
      v-bind="$attrs"
      binary
      :pt="preset"
      :pt-options="{ mergeSections: true, mergeProps: true }"
    />
    <label
      class="ml-2"
      :for="$attrs.id as string"
    >
      <slot name="label" />
    </label>
  </div>
</template>
