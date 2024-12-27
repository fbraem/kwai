<script setup lang="ts">
import Tag from 'primevue/tag';

interface Props {
  value?: string | null,
  rounded?: boolean,
  severity?: 'info' | 'warning' | 'success' | 'danger' | 'secondary',
}
withDefaults(defineProps<Props>(), { value: null, rounded: false, severity: undefined });
</script>

<template>
  <Tag
    :rounded
    :severity="severity"
    :value="value"
  >
    <slot />
  </Tag>
</template>

<style scoped>

</style>
