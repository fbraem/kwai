<script setup lang="ts">
import {
  CheckIcon, KwaiInputField, KwaiButton, KwaiCard, KwaiErrorAlert,
} from '@kwai/ui';
import { useForm } from 'vee-validate';
import { useHttpLogin } from '@kwai/api';
import {
  computed, type Ref,
} from 'vue';
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
import NotificationMessage from '@root/components/NotificationMessage.vue';
import { useLocalStorage } from '@vueuse/core';
import GoogleIcon from '@root/components/icons/GoogleIcon.vue';

const { t } = useI18n({ useScope: 'global' });

function isRequired(value: string): string | boolean {
  if (value && value.trim()) {
    return true;
  }
  return t('login.required');
}

function isEmail(value: string): string | boolean {
  const regex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i;
  if (!regex.test(value)) {
    return t('login.invalid_email');
  }
  return true;
}

const { handleSubmit } = useForm({
  validationSchema: {
    email: [isRequired, isEmail],
    password: isRequired,
  },
});

const redirect = useLocalStorage('login_redirect', null);
const googleUrl = computed(() => {
  const url = '/api/v1/auth/sso/google/login?return_url=';
  if (redirect.value) {
    return `${url}${redirect.value}`;
  }
  return `${url}/`;
});

const errorMessage: Ref<string | null> = ref(null);
const onSubmitForm = handleSubmit(async(values) => {
  errorMessage.value = null;
  const formData = {
    username: values.email,
    password: values.password,
  };
  await useHttpLogin(formData)
    .then(() => {
      showNotification.value = true;
      setTimeout(() => {
        showNotification.value = false;
        if (redirect.value) {
          const redirectUrl = redirect.value;
          redirect.value = null;
          window.location.replace(redirectUrl);
        } else {
          window.location.replace('/');
        }
      }, 3000);
    })
    .catch((error) => {
      if (error.response.status === 401) {
        errorMessage.value = t('login.failed');
      } else {
        errorMessage.value = t('login.error');
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
    {{ t('login.notifications.logged_in') }}
  </NotificationMessage>
  <div class="mb-6">
    <div class="mb-3">
      <h6 class="text-gray-900 text-2xl font-bold">
        {{ t('login.title') }}
      </h6>
      <p
        v-if="$kwai.admin"
        class="text-sm text-gray-500"
      >
        {{ t('login.need_account') }}
        <a
          class="text-blue-400 font-medium"
          :href="`mailto:${$kwai.admin.email}`"
        >
          {{ t('login.contact_us') }}
        </a>
      </p>
    </div>
  </div>
  <form
    class="flex-auto"
    @submit="onSubmitForm"
  >
    <KwaiInputField
      name="email"
      :placeholder="t('login.form.email.placeholder')"
      class="mb-6"
      :required="true"
    >
      <template #label>
        {{ t('login.form.email.label') }}
      </template>
    </KwaiInputField>
    <KwaiInputField
      name="password"
      type="password"
      :placeholder="t('login.form.password.placeholder')"
      :required="true"
    >
      <template #label>
        {{ t('login.form.password.label') }}
      </template>
    </KwaiInputField>
    <p class="text-right text-sm mt-1">
      <router-link
        class="text-blue-400"
        to="recover"
      >
        {{ t('login.forgotten') }}
      </router-link>
    </p>
    <KwaiErrorAlert
      v-if="errorMessage"
      class="mt-2"
    >
      <div class="text-sm">
        {{ errorMessage }}
      </div>
    </KwaiErrorAlert>
    <div class="flex flex-col items-end mt-6">
      <KwaiButton
        id="submit"
        :method="onSubmitForm"
        type="submit"
      >
        {{ t('login.form.submit.label') }}
      </KwaiButton>
    </div>
    <KwaiCard class="mt-10">
      <div class="flex flex-col sm:flex-row gap-2 items-center">
        <div class="text-sm">
          {{ t('login.google.description') }}
        </div>
        <KwaiButton
          :href="googleUrl"
          small
        >
          <template #icon>
            <GoogleIcon class="w-4 fill-current" />
          </template>
          {{ t('login.google.button') }}
        </KwaiButton>
      </div>
    </KwaiCard>
  </form>
</template>
