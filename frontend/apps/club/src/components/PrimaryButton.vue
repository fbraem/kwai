<script setup lang="ts">
import type { LocationAsRelativeRaw, RouteRecord } from 'vue-router';
import { LinkTag } from '@kwai/ui';

interface Props {
  route?: RouteRecord | LocationAsRelativeRaw,
  url?: string
}
defineProps<Props>();
</script>

<template>
  <LinkTag
    :route="route"
    :url="url"
    class="px-3 py-2 font-medium text-sm outline-none focus:outline-none rounded border border-green-500 text-gray-600 bg-green-500 hover:bg-white hover:text-black focus:ring-2 focus:ring-green-500"
  >
    <slot />
  </LinkTag>
</template>

<style scoped>

</style>
