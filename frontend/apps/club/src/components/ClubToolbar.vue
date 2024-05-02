<script setup lang="ts">

import { website } from '@kwai/config';
// eslint-disable-next-line import/no-absolute-path
import logoUrl from '/logo.png';
import type { MenuItem } from '@kwai/ui';
import { ToolbarLogo, ToolbarMenu } from '@kwai/ui';
import { useRouter } from 'vue-router';
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import PrimaryButton from '@root/components/PrimaryButton.vue';
import { isLoggedIn, useHttpLogout } from '@kwai/api';

const { t } = useI18n({ useScope: 'global' });

const router = useRouter();
const menuItems = computed(() : MenuItem[] => {
  const result: MenuItem[] = [];
  for (const route of router.getRoutes()) {
    if (route.meta.title) {
      result.push({
        title: route.meta.title as string,
        route,
      });
    }
  }
  return result;
});

const loggedIn = isLoggedIn;
const logout = () => {
  useHttpLogout();
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
          <div v-if="loggedIn">
            <PrimaryButton :method="logout">
              Logout
            </PrimaryButton>
          </div>
          <div v-else>
            <PrimaryButton :url="`${website.url}/apps/auth/login`">
              Login
            </PrimaryButton>
          </div>
        </div>
      </div>
    </div>
  </header>
  <ToolbarMenu
    :menu-items="menuItems"
    item-class="text-gray-600 hover:text-black"
  />
</template>

<style scoped>

</style>
