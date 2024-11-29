<script setup lang="ts">
import { toRef, useSlots } from 'vue';
import { useField } from 'vee-validate';
import RequiredIcon from '../icons/RequiredIcon.vue';
import DatePicker from 'primevue/datepicker';
import Slider from 'primevue/slider';

interface Props {
  name: string,
  id?: string,
  placeholder?: string
  format?: string
  time?: boolean
  required?: boolean
  partial?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  id: undefined,
  placeholder: '',
  format: 'dd-mm-yy',
  partial: true,
  required: false,
  time: false,
});
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
      :placeholder="placeholder"
      selection-mode="range"
      :manual-input="false"
      :date-format="format"
      :partial-range="partial"
      :show-time="time"
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

<style scoped>
.dp__main  {
  @apply w-72;
}
</style>
