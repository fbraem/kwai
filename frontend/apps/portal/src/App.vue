<template>
  <router-view />
</template>

<script setup lang="ts">
import { useApplicationStore } from '@root/stores/applicationStore';

const store = useApplicationStore();
store.load();
</script>
