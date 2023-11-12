<script setup lang="ts">
import { computed } from 'vue';
import type { RouteRecord } from 'vue-router';

interface Props {
  route?: RouteRecord,
  url?: string,
  method?: () => void
}
const props = defineProps<Props>();

const tag = computed(() => props.route ? 'router-link' : props.url ? 'a' : 'button');
const to = computed(() => props.route ? 'to' : null);
const href = computed(() => props.url ? 'href' : null);
const click = computed(() => props.method ? 'click' : null);
</script>

<template>
  <component
    :is="tag"
    :[to]="route"
    :[href]="url"
    @[click]="method"
  >
    <slot />
  </component>
</template>

<style scoped>

</style>
