<script setup lang="ts">
import {
  KwaiButton, KwaiErrorAlert, KwaiInputField, KwaiLoadBoundary,
  KwaiApiErrorBoundary,
} from '@kwai/ui';
import { useHttp } from '@kwai/api';
import { useI18n } from 'vue-i18n';
import { useTitle } from '@vueuse/core';
import { useForm } from 'vee-validate';
import type { Ref } from 'vue';
import { ref } from 'vue';
import {
  useRoute, useRouter,
} from 'vue-router';
import { useUserInvitation } from '../composables/useUserInvitations';
import { now } from '@kwai/date';

const { t } = useI18n({ useScope: 'global' });
useTitle(`Kwai | ${t('invited.title')}`);

const uuid = ref(useRoute().query.uuid);

const { data: userInvitation, isLoading, error } = useUserInvitation({ id: uuid });

function isRequired(value: string): string | boolean {
  if (value && value.trim()) {
    return true;
  }
  return t('invited.required');
}

function isSame(
  value: string,
  { form: { password } }: { form: { password: string } }
): string | boolean {
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
const errorMessage: Ref<string | null> = ref(null);
const onSubmitForm = handleSubmit(async(values) => {
  errorMessage.value = null;
  await useHttp()
    .url('/v1/auth/users')
    .json({
      data: {
        type: 'user_accounts',
        attributes: {
          first_name: values.firstName,
          last_name: values.lastName,
          password: values.password,
          remark: '',
        },
        relationships: {
          user_invitation: {
            data: {
              id: values.uuid,
              type: 'user_invitations',
            },
          },
        },
      },
    })
    .post()
    .res(() => router.push({ path: '/' }))
    .catch((error) => {
      if (error.response?.status === 422) {
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
        {{ t('invited.problem') }}
        <a
          class="text-blue-400 font-medium"
          href="#"
        >{{
          t('invited.contact_us')
        }}</a>
      </p>
    </div>
  </div>
  <KwaiLoadBoundary :loading="isLoading">
    <KwaiApiErrorBoundary
      :error="error"
      :email="$kwai.admin?.email"
    >
      <template #message>
        {{ t('invited.error_loading_invitation') }}
      </template>
      <KwaiErrorAlert v-if="userInvitation && (userInvitation.expiredAt.isBefore(now()) || userInvitation.confirmedAt)">
        {{ t('invited.expired') }}
      </KwaiErrorAlert>
      <form
        v-else
        class="flex-auto"
      >
        <div
          v-if="uuid === undefined"
          class="mb-6"
        >
          <KwaiInputField
            name="uuid"
            type="text"
            :placeholder="t('invited.form.uuid.placeholder')"
            :required="true"
          >
            <template #label>
              {{ t('invited.form.uuid.label') }}
            </template>
          </KwaiInputField>
          <p class="text-xs text-gray-500 mt-2">
            {{ t('invited.form.uuid.help') }}
          </p>
        </div>
        <div class="grid grid-cols-2 mb-6 gap-4">
          <KwaiInputField
            id="first_name"
            name="firstName"
            type="text"
            :placeholder="t('invited.form.first_name.placeholder')"
            :required="true"
          >
            <template #label>
              {{ t('invited.form.first_name.label') }}
            </template>
          </KwaiInputField>
          <KwaiInputField
            id="last_name"
            name="lastName"
            type="text"
            :placeholder="t('invited.form.last_name.placeholder')"
            :required="true"
          >
            <template #label>
              {{ t('invited.form.last_name.label') }}
            </template>
          </KwaiInputField>
        </div>
        <KwaiInputField
          name="password"
          type="password"
          :placeholder="t('invited.form.password.placeholder')"
          :required="true"
        >
          <template #label>
            {{ t('invited.form.password.label') }}
          </template>
        </KwaiInputField>
        <p class="text-xs text-gray-500 mt-2 mb-6">
          {{ t('invited.form.password.help') }}
        </p>
        <KwaiInputField
          name="repeat_password"
          type="password"
          :placeholder="t('invited.form.repeat_password.placeholder')"
          :required="true"
        >
          <template #label>
            {{ t('invited.form.repeat_password.label') }}
          </template>
        </KwaiInputField>
        <KwaiErrorAlert
          v-if="errorMessage"
          class="w-full mt-4"
        >
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
            {{ t('invited.form.submit.label') }}
          </KwaiButton>
        </div>
      </form>
    </KwaiApiErrorBoundary>
  </kwailoadboundary>
</template>
