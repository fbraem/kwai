<!-- A wrapper around PrimeVue Button -->
<script setup lang="ts">
import Button from 'primevue/button';
import type {
  LocationAsRelativeRaw, RouteRecord,
} from 'vue-router';
import {
  computed, useAttrs,
} from 'vue';

interface Props {
  to?: RouteRecord | LocationAsRelativeRaw
  method?: (event: Event | undefined) => void
  small?: boolean
  severity?: string
  variant?: 'text' | 'link'
  rounded?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  to: undefined,
  method: undefined,
  small: false,
  primary: true,
  severity: undefined,
  variant: undefined,
  rounded: false,
});

const attrs = useAttrs();
defineOptions({ inheritAttrs: false });

const tag = computed(() =>
  attrs.href ? 'a' : props.to ? 'router-link' : 'button'
);
const clickAttr = computed(() => (props.method ? 'click' : null));
const size = computed(() => (props.small ? 'small' : 'large'));
</script>

<template>
  <Button
    v-bind="$attrs"
    :size="size"
    :as="tag"
    :to="to"
    @[clickAttr]="(event: Event) => method(event)"
    :rounded="rounded"
    :severity="severity"
    :variant="variant"
  >
    <slot name="icon" />
    <slot />
  </Button>
</template>

<style scoped></style>
