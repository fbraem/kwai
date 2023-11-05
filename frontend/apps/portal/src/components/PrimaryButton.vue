<script setup lang="ts">
import { computed } from 'vue';
import type { RouteRecord } from 'vue-router';

interface Props {
  route?: RouteRecord,
  method?: () => void
}
const props = defineProps<Props>();

const tag = computed(() => props.route ? 'router-link' : 'button');
const to = computed(() => props.route ? 'to' : null);
const click = computed(() => props.method ? 'click' : null);
</script>

<template>
  <component
    :is="tag"
    class="px-3 py-1 font-medium text-sm outline-none focus:outline-none rounded border border-red-600 text-white bg-red-600 hover:bg-white hover:text-red-600 focus:ring-2 focus:ring-red-300"
    :[to]="route"
    @[click]="method"
  >
    <slot />
  </component>
</template>

<style scoped>

</style>
