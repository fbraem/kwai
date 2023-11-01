<script setup lang="ts">
import { useApplicationStore } from '../stores/applicationStore';
import { computed } from 'vue';

interface Props {
  filter?: string[]
}
const props = withDefaults(
  defineProps<Props>(), {
    filter: () => [],
  }
);

const store = useApplicationStore();
store.load();

const applications = computed(() => {
  // When application names are passed to the filter property,
  // only those applications matching the names will be returned.
  // The result will also be sorted in the order of the filter array.
  if (props.filter.length > 0) {
    const result = store.applications.filter(application => props.filter.includes(application.name));
    return result.sort(function(a, b) {
      return props.filter.indexOf(a.name) - props.filter.indexOf(b.name);
    });
  }
  return store.applications;
});
</script>

<template>
  <slot :applications="applications" />
</template>
