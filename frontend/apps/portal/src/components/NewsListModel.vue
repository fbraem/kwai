<!-- A renderless component for loading news stories -->
<template>
  <slot :stories="stories" />
</template>

<script setup lang="ts">
import type { Ref } from 'vue';
import { computed, ref } from 'vue';
import { useNewsStore, usePromotedNewsStore } from '@root/stores/newsStore';

interface Props {
  promoted?: boolean,
  application?: string|null,
}
const props = withDefaults(
  defineProps<Props>(), {
    promoted: false,
    application: null,
  }
);

const store = props.promoted ? usePromotedNewsStore() : useNewsStore();

const applicationId = ref(props.application);

if (props.application != null) {
  store.load({
    application: applicationId as Ref<string>,
  });
} else {
  store.load();
}

const stories = computed(() => store.items);
</script>
