<template>
  <div>
    <a :href="website.url">
      <div class="flex flex-row items-center">
        <img
          :src="logoUrl"
          class="w-16 mr-4"
          alt="logo"
        >
        <div class="text-xl font-medium uppercase">
          {{ website.title }}
        </div>
      </div>
    </a>
  </div>
</template>

<script lang="ts" setup>
// eslint-disable-next-line import/no-absolute-path
import logoUrl from '/logo.png';
import { website } from '@kwai/config';
</script>
