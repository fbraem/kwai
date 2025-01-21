<script setup lang="ts">
import { website } from '@kwai/config';
import logoUrl from '/logo.png';
import {
  KwaiAuthenticateButton, KwaiMenubar, ToolbarLogo, useMenu,
} from '@kwai/ui';
import { useI18n } from 'vue-i18n';
import {
  isLoggedIn, useHttpLogout,
} from '@kwai/api';

const { t } = useI18n({ useScope: 'global' });

const menuItems = useMenu();

const logout = async() => {
  await useHttpLogout();
  window.location.reload();
};
</script>

<template>
  <header class="container mx-auto p-8 lg:px-6 lg:max-w-6xl">
    <div class="grid grid-flow-row lg:grid-flow-col space-y-4 items-center">
      <ToolbarLogo
        :url="website.url"
        :logo="logoUrl"
      >
        {{ website.title }}
      </ToolbarLogo>
      <div class="flex flex-col md:flex-row md:items-center">
        <div class="md:w-2/3">
          <h2 class="font-medium text-xl">
            {{ t('home.title') }}
          </h2>
          <p class="text-sm text-gray-600">
            {{ t('home.description') }}
          </p>
        </div>
        <div class="flex flex-col place-items-end md:w-1/3">
          <KwaiAuthenticateButton
            :logged-in="isLoggedIn"
            :logout="logout"
          />
        </div>
      </div>
    </div>
  </header>
  <KwaiMenubar :items="menuItems" />
</template>

<style scoped></style>
