<!-- A wrapper around PrimeVue Button -->
<script setup lang="ts">
import Button from 'primevue/button';
import { LocationAsRelativeRaw, RouteRecord } from 'vue-router';
import { computed, useAttrs } from 'vue';
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

const wrapperTag = computed(() => attrs.href ? 'a' : props.to ? 'router-link' : null);
const clickAttr = computed(() => props.method ? 'click' : null);

const size = computed(() => props.small ? 'small' : undefined);
</script>

<template>
  <component
    :is="wrapperTag"
    v-if="wrapperTag"
    :to="to"
    :href="$attrs.href"
  >
    <Button
      v-bind="$attrs"
      :size="size"
      :pt="{
        root: {
          class: {
            'bg-primary-500': primary,
            'hover:bg-primary-600': primary,
            'text-primary-text': primary,
          }
        }
      }"
      :pt-options="{ mergeSections: false, mergeProps: true }"
    >
      <slot />
      <template #icon>
        <slot name="icon" />
      </template>
    </Button>
  </component>
  <Button
    v-else
    v-bind="$attrs"
    :size="size"
    :pt="{
      root: {
        class: {
          'bg-primary-500': primary,
          'hover:bg-primary-600': primary,
          'text-primary-text': primary,
        }
      }
    }"
    :pt-options="{ mergeSections: false, mergeProps: true }"
    @[clickAttr]="method"
  >
    <slot />
    <template #icon>
      <slot name="icon" />
    </template>
  </Button>
</template>

<style scoped>
</style>
