<script setup lang="ts">
import logoUrl from '/logo.png';
import { InformationDialog } from '@kwai/ui';
import config from '@kwai/config';

import { useI18n } from 'vue-i18n';
const { t } = useI18n({ useScope: 'global' });
</script>

<template>
  <InformationDialog>
    <template #information>
      <div class="flex flex-row sm:flex-col items-center">
        <div class="w-16 mr-2 sm:mb-4">
          <img
            :src="logoUrl"
            alt="logo"
          >
        </div>
        <h1 class="text-white text-2xl sm:text-center font-bold uppercase">
          {{ config.website.title }}
        </h1>
      </div>
      <p class="text-gray-300 my-6">
        {{ t('login.description.intro') }}
      </p>
      <p class="text-gray-300">
        {{ t('login.description.text') }}
      </p>
    </template>
    <router-view />
    <p class="mt-12 mb-3 text-center text-xs text-gray-500 justify-self-end">
      &copy; {{ config.website.copyright }}
    </p>
  </InformationDialog>
</template>
