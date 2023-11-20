<script setup lang="ts">
import { useTitle } from '@vueuse/core';
import { website } from '@kwai/config';

const title = useTitle();
title.value = `${website.title} | Author`;
</script>

<template>
  <router-view />
</template>
