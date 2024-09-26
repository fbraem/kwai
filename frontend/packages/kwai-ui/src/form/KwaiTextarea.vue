<script setup lang="ts">
import { toRef, useSlots } from 'vue';
import { useField } from 'vee-validate';
import Textarea from 'primevue/textarea';
import RequiredIcon from '../icons/RequiredIcon.vue';

const props = defineProps<{
  name: string,
  id?: string,
  type?: string,
  placeholder?: string
  required?: boolean
  rows?: number
}>();
const slots = useSlots();

const nameRef = toRef(props, 'name');
const { value, errorMessage } = useField<string>(nameRef);
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
    <Textarea
      :id="id ?? name"
      v-model="value"
      :rows="rows"
      :placeholder="placeholder ?? ''"
      auto-resize
      class="w-full"
      :invalid="!!errorMessage"
    />
    <small
      v-if="!!slots.help"
      :id="(id ?? name) + '-help'"
    >
      <slot name="help" />
    </small>
    <p
      v-if="errorMessage"
      class="mt-2 text-sm text-red-600"
    >
      {{ errorMessage }}
    </p>
  </div>
</template>
