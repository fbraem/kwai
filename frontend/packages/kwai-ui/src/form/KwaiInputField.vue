<script setup lang="ts">
import { toRef, useSlots } from 'vue';
import { useField } from 'vee-validate';
import RequiredIcon from '../icons/RequiredIcon.vue';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';

const props = defineProps<{
  name: string,
  type?: string,
  id?: string,
  placeholder?: string
  required?: boolean
}>();
const slots = useSlots();

const nameRef = toRef(props, 'name');
const { value, errorMessage } = useField<string|null>(nameRef);
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
    <div class="flex flex-col gap-2">
      <Password
        v-if="type === 'password'"
        :id="id ?? name"
        v-model="value"
        :placeholder="placeholder ?? ''"
        :feedback="false"
      />
      <InputText
        v-else
        :id="id ?? name"
        v-model="value"
        :placeholder="placeholder ?? ''"
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
  </div>
</template>
