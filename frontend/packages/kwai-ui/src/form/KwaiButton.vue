<!-- A wrapper around PrimeVue Button -->
<script setup lang="ts">
import Button from 'primevue/button';
import { LocationAsRelativeRaw, RouteRecord } from 'vue-router';
import { computed, useAttrs } from 'vue';
interface Props {
  to?: RouteRecord | LocationAsRelativeRaw,
  method?: () => void,
  small?: boolean,
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

const size = computed(() => props.small ? 'small' : undefined);
</script>

<template>
  <component
    :is="wrapperTag"
    v-if="wrapperTag"
    :[toAttr]="to"
    :[hrefAttr]="$attrs.href"
  >
    <Button
      v-bind="$attrs"
      :size="size"
    >
      <slot />
    </Button>
  </component>
  <Button
    v-else
    v-bind="$attrs"
    :size="size"
    @[clickAttr]="method"
  >
    <slot />
  </Button>
</template>

<style scoped>
</style>
