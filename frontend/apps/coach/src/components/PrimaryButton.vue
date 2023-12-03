<script setup lang="ts">
import type { LocationAsRelativeRaw, RouteRecord } from 'vue-router';
import { LinkTag } from '@kwai/ui';

interface Props {
  route?: RouteRecord | LocationAsRelativeRaw,
  url?: string,
  method?: () => void
}
defineProps<Props>();
</script>

<template>
  <LinkTag
    :route="route"
    :url="url"
    :method="method"
    class="px-3 py-2 font-medium text-sm text-white outline-none focus:outline-none rounded border border-orange-500 disabled:bg-orange-300 bg-orange-500 hover:bg-white hover:disabled:text-white hover:text-black focus:ring-2 focus:ring-orange-500"
  >
    <slot />
  </LinkTag>
</template>

<style scoped>

</style>
