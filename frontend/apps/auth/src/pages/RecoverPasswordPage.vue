<script setup lang="ts">
import { KwaiButton, KwaiErrorAlert, InputField } from '@kwai/ui';
import { useForm } from 'vee-validate';
import { useHttp } from '@kwai/api';
import type { Ref } from 'vue';
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useTitle } from '@vueuse/core';

const { t } = useI18n({ useScope: 'global' });
useTitle(`Kwai | ${t('recover_password.title')}`);

function isRequired(value: string): string|boolean {
  if (value && value.trim()) {
    return true;
  }
  return t('recover_password.required');
}

function isEmail(value: string): string|boolean {
  const regex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i;
  if (!regex.test(value)) {
    return t('recover_password.invalid_email');
  }
  return true;
}

const { handleSubmit } = useForm({
  validationSchema: {
    email: [isRequired, isEmail],
  },
});

const errorMessage: Ref<string|null> = ref(null);
const onSubmitForm = handleSubmit(async values => {
  errorMessage.value = null;
  const formData = {
    email: values.email,
  };
  await useHttp()
    .url('/auth/recover')
    .formData(formData)
    .post()
    .json()
    .catch(error => {
      if (error.response?.status === 401) {
        errorMessage.value = t('recover_password.failed');
      } else {
        console.log(error);
      }
    });
});
</script>

<template>
  <div class="mb-6">
    <div class="mb-3">
      <h6 class="text-gray-900 text-2xl font-bold">
        {{ t('recover_password.title') }}
      </h6>
      <p class="text-sm text-gray-500">
        {{ t('recover_password.problem') }} <a
          class="text-blue-400 font-medium"
          href="#"
        >{{ t('recover_password.contact_us') }}</a>
      </p>
    </div>
  </div>
  <form class="flex-auto">
    <InputField
      name="email"
      :placeholder="t('recover_password.form.email.placeholder')"
      class="mb-6"
      :required="true"
    >
      <template #label>
        {{ t('recover_password.form.email.label') }}
      </template>
    </InputField>
    <p class="text-xs text-gray-500">
      {{ t('recover_password.form.email.help') }}
    </p>
    <KwaiErrorAlert v-if="errorMessage">
      <div class="text-sm">
        {{ errorMessage }}
      </div>
    </KwaiErrorAlert>
    <div class="flex flex-col items-end mt-6">
      <KwaiButton
        id="submit"
        class="bg-gray-700 text-white"
        :method="onSubmitForm"
      >
        {{ t('recover_password.form.submit.label') }}
      </KwaiButton>
    </div>
  </form>
</template>
