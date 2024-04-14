<script setup lang="ts">
import { computed } from 'vue';

defineEmits(['click']);
interface Props {
  button?: boolean
}
const props = defineProps<Props>();

const tag = computed(() => props.button ? 'button' : 'a');
</script>

<template>
  <component
    :is="tag"
    class="hover:cursor-pointer text-sm font-bold px-12 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1"
    tabindex="0"
    @click="$emit('click')"
  >
    <slot />
  </component>
</template>
