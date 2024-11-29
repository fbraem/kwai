<script setup lang="ts">
import Checkbox from 'primevue/checkbox';
import { useSlots } from 'vue';

const model = defineModel<boolean>();
const slots = useSlots();
defineOptions({
  inheritAttrs: false,
});
</script>

<template>
  <div class="flex flex-col gap-2">
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
    <p
      v-if="!!slots.help"
      class="text-sm text-gray-500 py-2"
    >
      <slot name="help" />
    </p>
  </div>
</template>
