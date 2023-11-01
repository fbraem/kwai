<script setup lang="ts">
import { computed } from 'vue';
import { useApplications } from '@root/composables/useApplication';

interface Props {
  filter?: string[]
}
const props = withDefaults(
  defineProps<Props>(), {
    filter: () => [],
  }
);

const { data: applications } = useApplications();

const filteredApplications = computed(() => {
  // When application names are passed to the filter property,
  // only those applications matching the names will be returned.
  // The result will also be sorted in the order of the filter array.
  if (applications.value) {
    if (props.filter.length > 0) {
      const result = applications.value.filter(application => props.filter.includes(application.name));
      return result.sort(function(a, b) {
        return props.filter.indexOf(a.name) - props.filter.indexOf(b.name);
      });
    }
  }
  return applications.value;
});
</script>

<template>
  <slot :applications="filteredApplications" />
</template>
