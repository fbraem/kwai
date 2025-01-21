<script setup lang="ts">
import { useTitle } from '@vueuse/core';
import { getCurrentInstance } from 'vue';

const title = useTitle();
const $kwai = getCurrentInstance()?.appContext.config.globalProperties.$kwai;
if ($kwai) {
  title.value = `${$kwai.website.name} | Author`;
} else {
  title.value = 'Author';
}
</script>

<template>
  <router-view />
</template>
