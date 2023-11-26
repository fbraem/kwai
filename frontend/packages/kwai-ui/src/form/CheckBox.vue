<script setup lang="ts">
import { toRef, useSlots } from 'vue';
import { useField } from 'vee-validate';
import RequiredIcon from '../icons/RequiredIcon.vue';

const props = defineProps<{
  name: string,
  id?: string,
  required?: boolean,
  label?: string
}>();
const slots = useSlots();

const nameRef = toRef(props, 'name');
const { value, errorMessage } = useField(nameRef);
</script>
<template>
  <div class="flex flex-col">
    <div class="flex">
      <div>
        <input
          :id="id ?? name"
          v-model="value"
          type="checkbox"
          class="focus:ring-blue-600 h-4 w-4 rounded"
        >
      </div>
      <div>
        <label
          v-if="!!slots.label || label"
          :for="id ?? name"
          class="block pl-2"
        >
          <slot name="label" />
          <span v-if="label">{{ label }}</span>
          <RequiredIcon
            v-if="required"
            class="ml-1 w-2 h-2 -mt-4 fill-black"
          />
        </label>
      </div>
    </div>
    <p
      v-if="!!slots.help"
      class="text-sm text-gray-500 py-2"
    >
      <slot name="help" />
    </p>
    <p
      v-if="errorMessage"
      class="text-sm text-red-600 py-2"
    >
      {{ errorMessage }}
    </p>
  </div>
</template>
