<template>
  <div>
    <slot
      name="title"
      :loading="isLoading"
    />
    <template v-if="newsItems">
      <template v-if="newsItems.items.length === 0">
        <slot name="empty" />
      </template>
      <template
        v-for="newsItem in newsItems.items"
        v-else
      >
        <slot :news-item="newsItem" />
      </template>
    </template>
  </div>
</template>

<script setup lang="ts">
import { useNewsItems } from '@root/composables/useNewsItem';
interface Props {
  promoted?: boolean
}
const props = withDefaults(defineProps<Props>(), { promoted: false });

const { isLoading, data: newsItems } = useNewsItems({ promoted: props.promoted });

</script>
