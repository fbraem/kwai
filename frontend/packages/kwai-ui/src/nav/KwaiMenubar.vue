<script setup lang="ts">
import Menubar from 'primevue/menubar';
import { type MenuItem } from '../types';
import { computed } from 'vue';

interface Props {
  items: MenuItem[]
}
const properties = defineProps<Props>();

const menuItems = computed(() => {
  return properties.items.map(item => ({
    label: item.title,
    command: item.method,
    route: item.route,
    disabled: item.disabled ?? false,
  }));
});
</script>

<template>
  <Menubar
    :model="menuItems"
    :pt="{button: 'text-surface-0'}"
    class="bg-primary-400 w-full lg:px-6 lg:mx-auto lg:max-w-6xl"
  >
    <template #item="{ item, props, hasSubmenu }">
      <router-link
        v-if="item.route"
        v-slot="{ href, navigate }"
        :to="item.route"
        custom
      >
        <a
          :href="href"
          v-bind="props.action"
          class="flex items-center"
          @click="navigate"
        >
          <span :class="item.icon" />
          <span class="ml-2">{{ item.label }}</span>
        </a>
      </router-link>
      <a
        v-else
        :href="item.url"
        :target="item.target"
        v-bind="props.action"
      >
        <span :class="item.icon" />
        <span class="ml-2">{{ item.label }}</span>
        <span
          v-if="hasSubmenu"
          class="pi pi-fw pi-angle-down ml-2"
        />
      </a>
    </template>
  </Menubar>
</template>

<style scoped>
:deep(.p-menubar-item-link) {
  @apply bg-primary-500 hover:bg-primary-600 rounded text-surface-0;
}
</style>
