<script setup lang="ts">
import Panel from 'primevue/panel';
import {
  computed, useSlots,
} from 'vue';
import type { ApiError } from '../types';

interface Props {
  error: ApiError | Error | null
  email?: string
}
const props = defineProps<Props>();

const serverError = computed(() => props.error !== null && 'status' in props.error);
const slots = useSlots();
</script>

<template>
  <div
    v-if="error"
    class="mb-4"
  >
    <Panel
      collapsed
      :toggleable="serverError"
      :pt="{ header: () => 'bg-red-50/95 outline-red-200 text-red-600' }"
    >
      <template #header>
        <span class="font-bold">
          <slot name="message" />
        </span>
      </template>
      <dl
        v-if="serverError"
        class="border-1 rounded px-2 bg-white divide-y divide-gray-100 mb-2"
      >
        <div class="px-2 py-3 sm:grid sm:grid-cols-4 sm:gap-4 sm:px-0">
          <dt class="text-sm font-bold text-gray-900">
            Status
          </dt>
          <dd class="mt-1 text-sm/6 text-gray-700 sm:col-span-3 sm:mt-0">
            {{ (error as ApiError).status }}
          </dd>
        </div>
        <div class="px-2 py-3 sm:grid sm:grid-cols-4 sm:gap-4 sm:px-0">
          <dt class="text-sm font-bold text-gray-900">
            Error
          </dt>
          <dd class="mt-1 text-sm text-gray-700 sm:col-span-3 sm:mt-0">
            {{ (error as ApiError).message }}
          </dd>
        </div>
        <div class="px-2 py-3 sm:grid sm:grid-cols-4 sm:gap-4 sm:px-0">
          <dt class="text-sm font-bold text-gray-900">
            URL
          </dt>
          <dd class="mt-1 text-sm text-gray-700 sm:col-span-3 sm:mt-0">
            {{ (error as ApiError).url }}
          </dd>
        </div>
      </dl>
      <div
        class="py-2"
        v-if="email"
      >
        <slot name="email">
          <div class="text-xs">
            When the problem persists, contact our webmaster
            <a
              class="underline"
              :href="`mailto:${email}`"
            >
              {{ email }}
            </a>
          </div>
        </slot>
      </div>
    </Panel>
  </div>
  <div v-else-if="slots.default">
    <slot />
  </div>
</template>

<style scoped>

</style>
