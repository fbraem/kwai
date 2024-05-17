<script setup lang="ts">
import Checkbox from 'primevue/checkbox';

const model = defineModel<boolean>();

defineOptions({
  inheritAttrs: false,
});
</script>

<template>
  <div class="flex items-center">
    <Checkbox
      v-model="model"
      v-bind="$attrs"
      binary
    />
    <label
      class="ml-2"
      :for="$attrs.id as string"
    >
      <slot name="label" />
    </label>
  </div>
</template>
