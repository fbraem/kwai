<script setup lang="ts">
import Button from 'primevue/button';
import { LocationAsRelativeRaw, RouteRecord } from 'vue-router';
import { computed, useAttrs } from 'vue';
interface Props {
  to?: RouteRecord | LocationAsRelativeRaw,
  method?: () => void
}
const props = defineProps<Props>();

const attrs = useAttrs();
defineOptions({
  inheritAttrs: false,
});

const wrapperTag = computed(() => attrs.href ? 'a' : props.to ? 'router-link' : null);
const toAttr = computed(() => props.to ? 'to' : null);
const hrefAttr = computed(() => attrs.href ? 'href' : null);
const clickAttr = computed(() => props.method ? 'click' : null);
</script>

<template>
  <component
    :is="wrapperTag"
    v-if="wrapperTag"
    :[toAttr]="to"
    :[hrefAttr]="$attrs.href"
  >
    <Button v-bind="$attrs">
      <slot />
    </Button>
  </component>
  <Button
    v-else
    v-bind="$attrs"
    @[clickAttr]="method"
  >
    <slot />
  </Button>
</template>

<style scoped>
</style>
