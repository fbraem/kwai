<script setup lang="ts">
import { toRef, useSlots } from 'vue';
import { useField } from 'vee-validate';
import RequiredIcon from '../icons/RequiredIcon.vue';

const props = defineProps<{
  name: string,
  id?: string,
  type?: string,
  placeholder?: string
  required?: boolean
}>();
const slots = useSlots();

const nameRef = toRef(props, 'name');
const { value, errorMessage } = useField(nameRef);
</script>

<template>
  <div>
    <label
      v-if="!!slots.label"
      :for="id ?? name"
      class="block mb-2"
    >
      <slot name="label" />
      <RequiredIcon
        v-if="required"
        class="ml-1 w-2 h-2 -mt-4 fill-black"
      />
    </label>
    <input
      :id="id ?? name"
      v-model="value"
      :type="type ?? 'text'"
      class="border text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500"
      :class="{ 'mt-1': !!slots.label, 'border-red-600': errorMessage, 'focus:ring-red-600': errorMessage, 'focus:border-red-600': errorMessage }"
      :placeholder="placeholder ?? ''"
    >
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
