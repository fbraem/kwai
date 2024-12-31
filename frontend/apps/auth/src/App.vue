<script setup lang="ts">
import { DialogLayout } from '@kwai/ui';
import heroImageUrl from '/hero.jpg';
</script>

<template>
  <DialogLayout :image="heroImageUrl">
    <router-view />
  </DialogLayout>
  <div
    id="notify"
    class="absolute bottom-0 w-full z-10"
  />
</template>
