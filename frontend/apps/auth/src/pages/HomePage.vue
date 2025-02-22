<script setup lang="ts">
import {
  isLoggedIn, useHttpLogout,
} from '@kwai/api';
import { useI18n } from 'vue-i18n';
import ActionPanel from '@root/components/ActionPanel.vue';
const { t } = useI18n({ useScope: 'global' });

const logout = () => {
  useHttpLogout();
};
</script>

<template>
  <div class="flex-grow">
    <div class="mb-6">
      <h6 class="text-gray-900 text-2xl font-bold">
        {{ t('home.title') }}
      </h6>
      <p class="text-sm text-gray-500">
        {{ t('home.problem') }}
        <a
          class="text-blue-400 font-medium"
          href="#"
        >
          {{ t('home.contact_us') }}
        </a>
      </p>
    </div>
    <div>
      <h2 class="text-2xl text-gray-800 mb-3">
        Welke actie wil je uitvoeren?
      </h2>
      <ul>
        <li v-if="isLoggedIn()">
          <ActionPanel :method="logout">
            <template #title>
              {{ t('home.logout.title') }}
            </template>
            <template #description>
              {{ t('home.logout.description') }}
            </template>
          </ActionPanel>
        </li>
        <li v-else>
          <ActionPanel :route="{ name: 'login' }">
            <template #title>
              {{ t('home.login.title') }}
            </template>
            <template #description>
              {{ t('home.login.description') }}
            </template>
          </ActionPanel>
        </li>
        <li v-if="isLoggedIn()">
          <ActionPanel :route="{ name: 'change' }">
            <template #title>
              {{ t('home.change_password.title') }}
            </template>
            <template #description>
              {{ t('home.change_password.description') }}
            </template>
          </ActionPanel>
        </li>
        <li v-if="!isLoggedIn">
          <ActionPanel :route="{ name: 'recover' }">
            <template #title>
              {{ t('home.forgot_password.title') }}
            </template>
            <template #description>
              {{ t('home.forgot_password.description') }}
            </template>
          </ActionPanel>
        </li>
      </ul>
    </div>
  </div>
</template>
