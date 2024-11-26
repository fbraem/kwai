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
const { value, errorMessage } = useField(nameRef);
if (value.value == null) {
  value.value = 0;
}

const preset = {
  root: () => ({
    class: ['bg-primary-500'],
  }),
  handle: () => ({
    class: ['bg-primary-500'],
  }),
};
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
        :pt="preset"
        :pt-options="{ mergeSections: false, mergeProps: true }"
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
