<script setup lang="ts">
import { computed } from 'vue';
import type { LocationAsRelativeRaw, RouteRecord } from 'vue-router';

interface Props {
  route?: RouteRecord | LocationAsRelativeRaw,
  url?: string,
  method?: () => void
}
const props = defineProps<Props>();

const tag = computed(() => props.route ? 'router-link' : 'a');
const click = computed(() => props.method ? 'click' : null);
</script>

<template>
  <component
    :is="tag"
    :to="route"
    :href="url"
    @[click]="method"
  >
    <slot />
  </component>
</template>

<style scoped>

</style>
