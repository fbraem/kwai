<script setup lang="ts">
import Panel from 'primevue/panel';

interface Props {
  toggleable?: boolean
  headerClass?: string
}

withDefaults(defineProps<Props>(), {
  toggleable: false,
  headerClass: '',
});
</script>

<template>
  <Panel
    :toggleable="toggleable"
    :pt="{
      header: () => headerClass,
      headerActions: () => 'flex align-items-center',
    }"
    class="w-full"
  >
    <template
      v-if="$slots.header"
      #header
    >
      <slot name="header" />
    </template>
    <template
      v-if="$slots.footer"
      #footer
    >
      <slot name="footer" />
    </template>
    <template
      v-if="$slots.icons"
      #icons
    >
      <slot name="icons" />
    </template>
    <slot />
  </Panel>
</template>

<style scoped></style>
