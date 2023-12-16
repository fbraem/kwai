<script setup lang="ts">
import { computed, toRef, useSlots } from 'vue';
import { useField } from 'vee-validate';
import RequiredIcon from '../icons/RequiredIcon.vue';
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';

const props = defineProps<{
  name: string,
  id?: string,
  placeholder?: string
  format?: string
  required?: boolean
}>();
const slots = useSlots();

const nameRef = toRef(props, 'name');
const { value, errorMessage } = useField(nameRef);

const format = computed(() => props.format ?? 'HH:mm');
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
    <VueDatePicker
      :id="id ?? name"
      v-model="value"
      :format="format"
      time-picker
      text-input
      :placeholder="placeholder ?? ''"
      :class="{ 'mt-1': !!slots.label, 'border-red-600': errorMessage, 'focus:ring-red-600': errorMessage, 'focus:border-red-600': errorMessage }"
    />
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
