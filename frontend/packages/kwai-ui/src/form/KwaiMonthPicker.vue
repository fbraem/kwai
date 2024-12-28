<script setup lang="ts">
import { toRef, useSlots } from 'vue';
import { useField } from 'vee-validate';
import RequiredIcon from '../icons/RequiredIcon.vue';
import DatePicker from 'primevue/datepicker';

interface Props {
  name: string,
  id?: string | null,
  placeholder?: string
  format?: string
  required?: boolean
}

const props = withDefaults(
  defineProps<Props>(),
  {
    id: null,
    placeholder: '',
    format: 'mm-yy',
    required: false,
  }
);
const slots = useSlots();

const nameRef = toRef(props, 'name');
const { value, errorMessage } = useField<Date>(nameRef);
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
    <DatePicker
      :id="id ?? name"
      v-model="value"
      :date-format="format"
      view="month"
      :placeholder="placeholder ?? ''"
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
