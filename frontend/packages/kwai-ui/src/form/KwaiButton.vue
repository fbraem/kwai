<!-- A wrapper around PrimeVue Button -->
<script setup lang="ts">
import Button from 'primevue/button';
import { LocationAsRelativeRaw, RouteRecord } from 'vue-router';
import { computed, useAttrs, useSlots } from 'vue';
interface Props {
  to?: RouteRecord | LocationAsRelativeRaw,
  method?: () => void,
  small?: boolean,
  primary?: boolean
}
const props = withDefaults(
  defineProps<Props>(),
  { to: undefined, method: undefined, small: false, primary: true }
);

const attrs = useAttrs();
defineOptions({
  inheritAttrs: false,
});

const tag = computed(() => attrs.href ? 'a' : props.to ? 'router-link' : 'button');
const clickAttr = computed(() => props.method ? 'click' : null);
const slots = useSlots();

const size = computed(() => props.small ? 'small' : 'large');
</script>

<template>
  <Button
    v-bind="$attrs"
    :size="size"
    :as="tag"
    :to="to"
    @[clickAttr]="method"
  >
    <slot />
    <template
      v-if="!!slots.icon"
      #icon
    >
      <slot name="icon" />
    </template>
  </Button>
</template>

<style scoped>
</style>
