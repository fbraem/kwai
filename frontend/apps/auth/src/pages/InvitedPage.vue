<script setup lang="ts">
import { KwaiButton, ErrorAlert, InputField } from '@kwai/ui';
import { useHttp } from '@kwai/api';
import { useI18n } from 'vue-i18n';
import { useTitle } from '@vueuse/core';
import { useForm } from 'vee-validate';
import type { Ref } from 'vue';
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const { t } = useI18n({ useScope: 'global' });
useTitle(`Kwai | ${t('invited.title')}`);

const uuid = ref(useRoute().query.uuid);

function isRequired(value: string): string|boolean {
  if (value && value.trim()) {
    return true;
  }
  return t('invited.required');
}

function isSame(value: string, { form: { password } } : { form: { password: string }}): string|boolean {
  if (value && value === password) {
    return true;
  }
  return t('invited.not_same');
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
    return t('invited.form.password.strength');
  }
  return true;
}

const { handleSubmit } = useForm({
  validationSchema: {
    uuid: [isRequired],
    firstName: [isRequired],
    lastName: [isRequired],
    password: [isRequired, isStrong],
    repeat_password: [isRequired, isSame],
  },
  initialValues: {
    uuid: uuid.value,
    firstName: '',
    lastName: '',
    password: '',
    repeat_password: '',
  },
});

const router = useRouter();
const expired: Ref<boolean> = ref(false);
const errorMessage: Ref<string|null> = ref(null);
const onSubmitForm = handleSubmit(async values => {
  errorMessage.value = null;
  await useHttp()
    .url(`/users/invitations/${values.uuid}`)
    .json({
      data: {
        type: 'user_invitations',
        id: values.uuid,
        attributes: {
          first_name: values.firstName,
          last_name: values.lastName,
          password: values.password,
          remark: '',
        },
      },
    })
    .post()
    .res(() => router.push({
      path: '/',
    }))
    .catch(error => {
      if (error.response?.status === 401) {
        errorMessage.value = t('invited.expired');
        expired.value = true;
      } else if (error.response?.status !== 200) {
        errorMessage.value = t('invited.failed');
      }
    });
});
</script>

<template>
  <div class="mb-6">
    <div class="mb-3">
      <h6 class="text-gray-900 text-2xl font-bold">
        {{ t('invited.title') }}
      </h6>
      <p class="text-sm text-gray-500">
        {{ t('invited.problem') }} <a
          class="text-blue-400 font-medium"
          href="#"
        >{{ t('invited.contact_us') }}</a>
      </p>
    </div>
  </div>
  <form class="flex-auto">
    <div
      v-if="uuid === undefined"
      class="mb-6"
    >
      <InputField
        name="uuid"
        type="text"
        :placeholder="t('invited.form.uuid.placeholder')"
        :required="true"
      >
        <template #label>
          {{ t('invited.form.uuid.label') }}
        </template>
      </InputField>
      <p class="text-xs text-gray-500 mt-2">
        {{ t('invited.form.uuid.help') }}
      </p>
    </div>
    <div class="grid grid-cols-2 mb-6 gap-4">
      <InputField
        id="first_name"
        name="firstName"
        type="text"
        :placeholder="t('invited.form.first_name.placeholder')"
        :required="true"
      >
        <template #label>
          {{ t('invited.form.first_name.label') }}
        </template>
      </InputField>
      <InputField
        id="last_name"
        name="lastName"
        type="text"
        :placeholder="t('invited.form.last_name.placeholder')"
        :required="true"
      >
        <template #label>
          {{ t('invited.form.last_name.label') }}
        </template>
      </InputField>
    </div>
    <InputField
      name="password"
      type="password"
      :placeholder="t('invited.form.password.placeholder')"
      :required="true"
    >
      <template #label>
        {{ t('invited.form.password.label') }}
      </template>
    </InputField>
    <p class="text-xs text-gray-500 mt-2 mb-6">
      {{ t('invited.form.password.help') }}
    </p>
    <InputField
      name="repeat_password"
      type="password"
      :placeholder="t('invited.form.repeat_password.placeholder')"
      :required="true"
    >
      <template #label>
        {{ t('invited.form.repeat_password.label') }}
      </template>
    </InputField>
    <div
      v-if="errorMessage"
      class="flex items-center gap-3"
    >
      <ErrorAlert class="w-full">
        <div class="text-sm">
          {{ errorMessage }}
        </div>
      </ErrorAlert>
      <div v-if="expired">
        <router-link
          :to="{ name: 'recover' }"
          class="text-blue-400 text-sm font-medium"
        >
          {{ t('invited.generate_code') }}
        </router-link>
      </div>
    </div>
    <div class="flex flex-col items-end mt-6">
      <KwaiButton
        id="submit"
        class="bg-gray-700 text-white"
        :method="onSubmitForm"
      >
        {{ t('invited.form.submit.label') }}
      </KwaiButton>
    </div>
  </form>
</template>
