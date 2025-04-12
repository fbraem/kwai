<script setup lang="ts">
import { useHttp } from '@kwai/api';
import {
  KwaiButton, KwaiErrorAlert, KwaiInputField,
} from '@kwai/ui';
import { useI18n } from 'vue-i18n';
import { useTitle } from '@vueuse/core';
import { useForm } from 'vee-validate';
import type { Ref } from 'vue';
import { ref } from 'vue';
import {
  useRoute, useRouter,
} from 'vue-router';

const { t } = useI18n({ useScope: 'global' });
useTitle(`Kwai | ${t('reset_password.title')}`);

const uuid = ref(useRoute().query.uuid);

function isRequired(value: string): string | boolean {
  if (value && value.trim()) {
    return true;
  }
  return t('reset_password.required');
}

function isSame(value: string, { form: { password } }: { form: { password: string } }): string | boolean {
  if (value && value === password) {
    return true;
  }
  return t('reset_password.not_same');
}

function isStrong(value: string) {
  let strength = 0;
  if (value) {
    if (value.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) {
      strength += 1;
    }
    if (value.match(/([0-9])/)) {
      strength += 1;
    }
    if (value.length > 7) {
      strength += 1;
    }
  }
  if (strength < 3) {
    return t('reset_password.form.password.strength');
  }
  return true;
}

const { handleSubmit } = useForm({
  validationSchema: {
    uuid: [isRequired],
    password: [isRequired, isStrong],
    repeat_password: [isRequired, isSame],
  },
  initialValues: {
    uuid: uuid.value,
    password: '',
    repeat_password: '',
  },
});

const router = useRouter();
const expired: Ref<boolean> = ref(false);
const errorMessage: Ref<string | null> = ref(null);
const onSubmitForm = handleSubmit(async(values) => {
  errorMessage.value = null;
  const formData = {
    uuid: values.uuid,
    password: values.password,
  };
  await useHttp()
    .url('/v1/auth/reset')
    .formData(formData)
    .post()
    .res(() => router.push({ path: '/' }))
    .catch((error) => {
      if (error.response?.status === 401) {
        errorMessage.value = t('reset_password.expired');
        expired.value = true;
      } else if (error.response?.status !== 200) {
        errorMessage.value = t('reset_password.failed');
      }
    });
});
</script>

<template>
  <div class="mb-6">
    <div class="mb-3">
      <h6 class="text-gray-900 text-2xl font-bold">
        {{ t('reset_password.title') }}
      </h6>
      <p class="text-sm text-gray-500">
        {{ t('reset_password.problem') }} <a
          class="text-blue-400 font-medium"
          href="#"
        >{{ t('reset_password.contact_us') }}</a>
      </p>
    </div>
  </div>
  <form class="flex-auto">
    <div
      v-if="uuid === undefined"
      class="mb-6"
    >
      <KwaiInputField
        name="uuid"
        type="text"
        :placeholder="t('reset_password.form.uuid.placeholder')"
        :required="true"
      >
        <template #label>
          {{ t('reset_password.form.uuid.label') }}
        </template>
      </KwaiInputField>
      <p class="text-xs text-gray-500 mt-2">
        {{ t('reset_password.form.uuid.help') }}
        <router-link
          :to="{ name: 'recover' }"
          class="text-blue-400 font-medium"
        >
          Genereer nieuwe code
        </router-link>
      </p>
    </div>
    <KwaiInputField
      name="password"
      type="password"
      :placeholder="t('reset_password.form.password.placeholder')"
      :required="true"
    >
      <template #label>
        {{ t('reset_password.form.password.label') }}
      </template>
    </KwaiInputField>
    <p class="text-xs text-gray-500 mt-2 mb-6">
      {{ t('reset_password.form.password.help') }}
    </p>
    <KwaiInputField
      name="repeat_password"
      type="password"
      :placeholder="t('reset_password.form.repeat_password.placeholder')"
      class="mb-6"
      :required="true"
    >
      <template #label>
        {{ t('reset_password.form.repeat_password.label') }}
      </template>
    </KwaiInputField>
    <div
      v-if="errorMessage"
      class="flex items-center gap-3"
    >
      <KwaiErrorAlert
        v-if="errorMessage"
      >
        <div class="text-sm">
          {{ errorMessage }}
        </div>
      </KwaiErrorAlert>
      <div v-if="expired">
        <router-link
          :to="{ name: 'recover' }"
          class="text-blue-400 text-sm font-medium"
        >
          {{ t('reset_password.generate_code') }}
        </router-link>
      </div>
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
