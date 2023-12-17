<script setup lang="ts">
import { website } from '@kwai/config';
</script>

<template>
  <div class="flex flex-col place-items-end">
    <div>
      <a
        :href="`${website.url}/auth/login`"
        class="px-3 py-2 flex items-center bg-red-600 text-white hover:bg-white hover:text-red-600 hover:cursor-pointer border border-red-600"
      >
        Login
      </a>
    </div>
  </div>
</template>
