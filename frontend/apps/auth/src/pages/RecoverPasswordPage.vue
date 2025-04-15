<script setup lang="ts">
import {
  KwaiButton, KwaiApiErrorBoundary,
  type ApiError,
  KwaiInputField,
} from '@kwai/ui';
import { useForm } from 'vee-validate';
import { useHttp } from '@kwai/api';
import type { Ref } from 'vue';
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useTitle } from '@vueuse/core';

const { t } = useI18n({ useScope: 'global' });
useTitle(`Kwai | ${t('recover_password.title')}`);

function isRequired(value: string): string | boolean {
  if (value && value.trim()) {
    return true;
  }
  return t('recover_password.required');
}

function isEmail(value: string): string | boolean {
  const regex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i;
  if (!regex.test(value)) {
    return t('recover_password.invalid_email');
  }
  return true;
}

const { handleSubmit } = useForm({ validationSchema: { email: [isRequired, isEmail] } });

const errorMessage: Ref<Error | ApiError | null> = ref(null);
const onSubmitForm = handleSubmit(async(values) => {
  errorMessage.value = null;
  const formData = { email: values.email };
  await useHttp()
    .url('/v1/auth/recover')
    .formData(formData)
    .post()
    .json()
    .catch((error) => {
      if (error.response) {
        errorMessage.value = {
          status: error.response.status,
          message: error.json.detail,
          url: error.response.url,
        };
      } else {
        errorMessage.value = error;
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
      <p
        v-if="$kwai.admin?.email"
        class="text-sm text-gray-500"
      >
        {{ t('recover_password.problem') }}
        <a
          class="text-blue-400 font-medium"
          :href="`mailto:${$kwai.admin.email}`"
        >
          {{ t('recover_password.contact_us') }}
        </a>
      </p>
    </div>
  </div>
  <form class="flex-auto">
    <KwaiInputField
      name="email"
      :placeholder="t('recover_password.form.email.placeholder')"
      class="mb-6"
      :required="true"
    >
      <template #label>
        {{ t('recover_password.form.email.label') }}
      </template>
    </KwaiInputField>
    <p class="text-xs text-gray-500">
      {{ t('recover_password.form.email.help') }}
    </p>
    <div
      v-if="errorMessage"
      class="m-2"
    >
      <KwaiApiErrorBoundary
        :error="errorMessage"
        :email="$kwai.admin?.email"
      >
        <template #message>
          <div>
            {{ errorMessage }}
          </div>
        </template>
      </KwaiApiErrorBoundary>
    </div>
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
