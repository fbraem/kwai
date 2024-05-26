<script setup lang="ts">
import Message from 'primevue/message';
interface Props {
  severity?: 'success' | 'info' | 'warn' | 'error',
  closable?: boolean
}
withDefaults(defineProps<Props>(), {
  severity: 'info',
  closable: false,
});
</script>

<template>
  <Message
    :severity="severity"
    :closable="closable"
  >
    <template #messageicon>
      <slot name="icon" />
    </template>
    <slot />
  </Message>
</template>
