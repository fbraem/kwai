<script setup lang="ts">
import { computed, getCurrentInstance, useAttrs } from 'vue';
import ButtonGroup from './ButtonGroup.vue';
import type { LocationAsRelativeRaw, RouteRecord } from 'vue-router';

defineEmits(['click']);
interface Props {
  to?: RouteRecord | LocationAsRelativeRaw
}
const props = defineProps<Props>();

const instance = getCurrentInstance();
const inButtonGroup = computed(() => {
  let result = false;
  if (instance && instance.parent) {
    result = instance.parent.type === ButtonGroup;
  }
  return result;
});
const attrs = useAttrs();
const htmlTag = computed(() => attrs.href ? 'a' : props.to ? 'router-link' : 'button');
const classObject = computed(() => ({
  rounded: !inButtonGroup.value,
  shadow: !inButtonGroup.value,
  'hover:shadow-lg': !inButtonGroup.value,
  'first:rounded-l-md': inButtonGroup.value,
  'last:rounded-r-md': inButtonGroup.value,
}));
</script>

<template>
  <component
    :is="htmlTag"
    class="hover:cursor-pointer text-sm border font-bold outline-none focus:outline-none"
    :class="classObject"
    tabindex="0"
    @click="$emit('click')"
  >
    <slot />
  </component>
</template>
