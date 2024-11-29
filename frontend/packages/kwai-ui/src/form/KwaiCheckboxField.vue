<script setup lang="ts">
import Checkbox from 'primevue/checkbox';
import { useField } from 'vee-validate';
import { toRef, useSlots } from 'vue';

const props = defineProps<{
  name: string,
  id?: string
}>();
const slots = useSlots();

defineOptions({
  inheritAttrs: false,
});

const nameRef = toRef(props, 'name');
const { value, errorMessage } = useField(nameRef);
</script>

<template>
  <div class="flex flex-col gap-2">
    <div class="flex items-center">
      <Checkbox
        v-model="value"
        v-bind="$attrs"
        binary
      />
      <label
        v-if="!!slots.label"
        class="ml-2"
        :for="id ?? name"
      >
        <slot name="label" />
      </label>
    </div>
    <p
      v-if="errorMessage"
      class="mt-2 text-sm text-red-600"
    >
      {{ errorMessage }}
    </p>
  </div>
</template>
