<template>
  <DialogLayout :image="heroImageUrl">
    <router-view />
  </DialogLayout>
  <div
    id="notify"
    class="absolute bottom-0 w-full z-10"
  />
</template>

<script setup lang="ts">
import { DialogLayout } from '@kwai/ui';
// eslint-disable-next-line import/no-absolute-path
import heroImageUrl from '/hero.jpg';
</script>
