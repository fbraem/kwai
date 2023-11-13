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
    class="px-3 py-1 font-medium text-sm outline-none focus:outline-none rounded border border-yellow-300 text-gray-600 bg-yellow-300 hover:bg-white hover:text-black focus:ring-2 focus:ring-yellow-300"
  >
    <slot />
  </LinkTag>
</template>

<style scoped>

</style>
