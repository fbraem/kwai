<script setup lang="ts">
import { toRef, useSlots } from 'vue';
import { useField } from 'vee-validate';
import Slider from 'primevue/slider';
import RequiredIcon from '../icons/RequiredIcon.vue';

const props = defineProps<{
  name: string,
  id?: string,
  required?: boolean
}>();
const slots = useSlots();

const nameRef = toRef(props, 'name');
const { value, errorMessage } = useField<number>(nameRef);
if (value.value == null) {
  value.value = 0;
}
</script>

<template>
  <div>
    <label
      :for="id ?? name"
      class="block mb-2 text-sm font-medium"
    >
      <slot name="label" />
      <RequiredIcon
        v-if="required"
        class="ml-1 w-2 h-2 -mt-4 fill-black"
      />
    </label>
    <div class="flex items-center space-x-4">
      <Slider
        :id="id ?? name"
        v-model="value"
        class="w-56"
      />
      <div>
        {{ value }}
      </div>
    </div>
    <p
      v-if="!!slots.help"
      class="mt-2 text-sm text-gray-500 dark:text-gray-400"
    >
      <slot name="help" />
    </p>
    <p
      v-if="errorMessage"
      class="mt-2 text-sm text-red-600"
    >
      {{ errorMessage }}
    </p>
  </div>
</template>
