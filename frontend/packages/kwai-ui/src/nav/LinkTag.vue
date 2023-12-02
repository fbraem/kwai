<script setup lang="ts">
import { computed } from 'vue';
import type { LocationAsRelativeRaw, RouteRecord } from 'vue-router';

interface Props {
  route?: RouteRecord | LocationAsRelativeRaw,
  url?: string,
  method?: () => void
}
const props = defineProps<Props>();

const tag = computed(() => props.route ? 'router-link' : props.url ? 'a' : 'button');
const to = computed(() => props.route ? 'to' : null);
const href = computed(() => props.url ? 'href' : null);
const click = computed(() => props.method ? 'click' : null);
const type = computed(() => tag.value === 'button' ? 'button' : null);
</script>

<template>
  <component
    :is="tag"
    :[to]="route"
    :[href]="url"
    :type="type"
    @[click]="method"
  >
    <slot />
  </component>
</template>

<style scoped>

</style>
