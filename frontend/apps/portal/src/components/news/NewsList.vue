<script setup lang="ts">
import { useNewsItems } from '@root/composables/useNewsItem';
import { ref } from 'vue';
interface Props {
  promoted?: boolean,
  application?: string | null
}
const props = withDefaults(defineProps<Props>(), { promoted: false, application: null });

const application = props.application ? ref(props.application) : null;

const { isLoading, data: newsItems } = useNewsItems({ promoted: props.promoted, application });
</script>

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
