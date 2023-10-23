<!-- A renderless component for loading news stories -->
<template>
  <slot
    :loading="isLoading"
    :news-items="data"
  />
</template>

<script setup lang="ts">
import { useNewsItems, usePromotedNewsItems } from '@root/composables/useNewsItem';

interface Props {
  promoted: Boolean
}
const props = defineProps<Props>();

const { isLoading, data } = (props.promoted) ? usePromotedNewsItems() : useNewsItems();
</script>
