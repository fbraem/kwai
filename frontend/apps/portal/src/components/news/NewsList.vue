<template>
  <NewsListModel
    v-slot="{ loading, newsItems }"
    :promoted="promoted"
  >
    <slot
      name="title"
      :loading="loading"
    />
    <template v-if="newsItems">
      <template v-if="newsItems.length === 0">
        <slot name="empty" />
      </template>
      <template
        v-for="newsItem in newsItems"
        v-else
      >
        <slot :news-item="newsItem" />
      </template>
    </template>
  </NewsListModel>
</template>

<script setup lang="ts">
import NewsListModel from './NewsListModel.vue';

import { toRefs } from 'vue';
interface Props {
  promoted: Boolean
}
const props = defineProps<Props>();
const { promoted } = toRefs(props);
</script>
