<template>
  <div class="text-center p-2 bg-red-600 text-white min-w-fit">
    <span class="block font-bold text-xl">
      {{ date.format('D') }}
    </span>
    <span class="block text-sm">
      {{ date.format('MMM') }}
    </span>
    <span class="block text-sm">
      {{ date.format('YYYY') }}
    </span>
  </div>
</template>

<script setup lang="ts">
import type { DateType } from '@kwai/date';

interface Props {
  date: DateType
}

defineProps<Props>();
</script>
