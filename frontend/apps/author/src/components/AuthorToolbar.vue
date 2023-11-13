<script setup lang="ts">
// eslint-disable-next-line import/no-absolute-path
import logoUrl from '/logo.png';
import { website } from '@kwai/config';
import type { MenuItem } from '@kwai/ui';
import { ToolbarLogo, ToolbarMenu } from '@kwai/ui';
import { useRouter } from 'vue-router';
import { computed } from 'vue';
import PrimaryButton from '@root/components/PrimaryButton.vue';

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
            Auteursomgeving
          </h2>
          <p class="text-sm text-gray-600">
            Beheer nieuws, pagina's, ...
          </p>
        </div>
        <div class="flex flex-col place-items-end md:w-1/3">
          <div>
            <PrimaryButton
              :url="`${website.url}/auth/login`"
              class="px-3 py-2 flex items-center bg-yellow-300 text-gray-800 hover:bg-white hover:text-black hover:cursor-pointer border border-yellow-300"
            >
              Login
            </PrimaryButton>
          </div>
        </div>
      </div>
    </div>
  </header>
  <ToolbarMenu
    :menu-items="menuItems"
    class="bg-yellow-300"
    item-class="text-gray-600 hover:text-black"
  />
</template>

<style scoped>

</style>
