<script setup lang="ts">
import { useHttpWithAuthCatcher } from '@kwai/api';
import {
  KwaiButton, CheckIcon, KwaiErrorAlert, KwaiInputField,
} from '@kwai/ui';
import { useI18n } from 'vue-i18n';
import { useTitle } from '@vueuse/core';
import { useForm } from 'vee-validate';
import type { Ref } from 'vue';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import NotificationMessage from '@root/components/NotificationMessage.vue';

const { t } = useI18n({ useScope: 'global' });
useTitle(`Kwai | ${t('change_password.title')}`);

function isRequired(value: string): string | boolean {
  if (value && value.trim()) {
    return true;
  }
  return t('change_password.required');
}

function isSame(value: string, { form: { password } }: { form: { password: string } }): string | boolean {
  if (value && value === password) {
    return true;
  }
  return t('change_password.not_same');
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
    password: [isRequired, isStrong],
    repeat_password: [isRequired, isSame],
  },
  initialValues: {
    password: '',
    repeat_password: '',
  },
});

const router = useRouter();
const errorMessage: Ref<string | null> = ref(null);
const onSubmitForm = handleSubmit(async(values) => {
  errorMessage.value = null;
  const formData = { password: values.password };
  await useHttpWithAuthCatcher()
    .url('/v1/auth/change')
    .formData(formData)
    .post()
    .res(() => {
      showNotification.value = true;
      setTimeout(() => {
        showNotification.value = false;
        router.push({ path: '/' });
      }, 3000);
    })
    .catch((error) => {
      if (error.response?.status !== 200) {
        errorMessage.value = t('change_password.failed');
      } else {
        console.log(error);
      }
    });
});

const showNotification = ref(false);
const closeNotification = () => {
  showNotification.value = false;
};
</script>

<template>
  <NotificationMessage
    v-if="showNotification"
    :can-be-closed="true"
    @close="closeNotification"
  >
    <CheckIcon class="w-8 h-8 mr-2 fill-green-600" />
    {{ t('change_password.notifications.password_changed') }}
  </NotificationMessage>
  <div class="mb-6">
    <div class="mb-3">
      <h6 class="text-gray-900 text-2xl font-bold">
        {{ t('change_password.title') }}
      </h6>
      <p
        v-if="$kwai.admin?.email"
        class="text-sm text-gray-500"
      >
        {{ t('change_password.problem') }} <a
          class="text-blue-400 font-medium"
          :href="`mailto:${$kwai.admin.email}`"
        >{{ t('change_password.contact_us') }}</a>
      </p>
    </div>
  </div>
  <form class="flex-auto">
    <KwaiInputField
      name="password"
      type="password"
      :placeholder="t('change_password.form.password.placeholder')"
      :required="true"
    >
      <template #label>
        {{ t('change_password.form.password.label') }}
      </template>
    </KwaiInputField>
    <p class="text-xs text-gray-500 mt-2 mb-6">
      {{ t('change_password.form.password.help') }}
    </p>
    <KwaiInputField
      name="repeat_password"
      type="password"
      :placeholder="t('change_password.form.repeat_password.placeholder')"
      class="mb-6"
      :required="true"
    >
      <template #label>
        {{ t('change_password.form.repeat_password.label') }}
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
    </div>
    <div class="flex flex-col items-end mt-6">
      <KwaiButton
        id="submit"
        class="bg-gray-700 text-white"
        :method="onSubmitForm"
      >
        {{ t('change_password.form.submit.label') }}
      </KwaiButton>
    </div>
  </form>
</template>
