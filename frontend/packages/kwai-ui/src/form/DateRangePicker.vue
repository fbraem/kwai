<script setup lang="ts">
import { toRef, useSlots } from 'vue';
import { useField } from 'vee-validate';
import RequiredIcon from '../icons/RequiredIcon.vue';
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';
import { createFromDate } from '@kwai/date';

interface Props {
  name: string,
  id?: string,
  placeholder?: string
  time?: boolean
  required?: boolean
  partial?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  id: undefined,
  placeholder: '',
  partial: true,
  required: false,
  time: false,
});
const slots = useSlots();

const nameRef = toRef(props, 'name');
const { value, errorMessage } = useField(nameRef);

const format = (dates: Date[]) : string => {
  const format = props.time ? 'L LTS' : 'L';
  let formattedRange = createFromDate(dates[0]).format(format);
  if (dates.length === 2) {
    if (dates[1]) {
      formattedRange += ' - ' + createFromDate(dates[1]).format(format);
    }
  }
  return formattedRange;
};
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
      :placeholder="placeholder"
      range
      :format="format"
      :class="{ 'mt-1': !!slots.label, 'border-red-600': errorMessage, 'focus:ring-red-600': errorMessage, 'focus:border-red-600': errorMessage }"
      :teleport="true"
      :partial-range="partial"
      :enable-time-picker="time"
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
