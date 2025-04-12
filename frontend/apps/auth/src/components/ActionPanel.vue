<script setup lang="ts">
import { computed } from 'vue';
import type { LocationQuery } from 'vue-router';

const props = defineProps<{
  route?: LocationQuery
  method?: Function
}>();

const tag = computed(() => props.route ? 'router-link' : 'a');
const to = computed(() => props.route ? 'to' : '');
const click = computed(() => props.method ? 'click' : '');
</script>

<template>
  <component
    :is="tag"
    class="block p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 hover:cursor-pointer"
    :[to]="route"
    @[click]="method"
  >
    <div class="font-semibold">
      <slot name="title" />
    </div>
    <span class="text-sm font-light text-gray-500 dark:text-gray-400">
      <slot name="description" />
    </span>
  </component>
</template>
