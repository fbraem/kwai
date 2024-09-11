<script setup lang="ts">
import { KwaiButton, ToolbarLogo, ToolbarMenu, useMenu } from '@kwai/ui';
import { website } from '@kwai/config';
// eslint-disable-next-line import/no-absolute-path
import logoUrl from '/logo.png';

const menuItems = useMenu();
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
            Coachomgeving
          </h2>
          <p class="text-sm text-gray-600">
            Beheer trainingen, teams, leden, ...
          </p>
        </div>
        <div class="flex flex-col place-items-end md:w-1/3">
          <div>
            <KwaiButton :href="`${website.url}/apps/auth/login`">
              Login
            </KwaiButton>
          </div>
        </div>
      </div>
    </div>
  </header>
  <ToolbarMenu
    :menu-items="menuItems"
    class="text-white bg-orange-500"
    item-class="hover:text-black"
  />
</template>

<style scoped>

</style>
