<script setup lang="ts">
import Badge from 'primevue/badge';
interface Props {
  value: string,
  size?: 'xlarge' | 'large' | 'small',
  severity?: 'info' | 'warning' | 'success' | 'danger'
}
withDefaults(defineProps<Props>(), { severity: 'info', size: 'small' });
</script>

<template>
  <Badge
    :value="value"
    :severity="severity"
  />
</template>

<style scoped>

</style>
