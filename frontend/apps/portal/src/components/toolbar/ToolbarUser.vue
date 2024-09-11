<script setup lang="ts">
import { website } from '@kwai/config';
import { KwaiButton } from '@kwai/ui';
</script>

<template>
  <div class="flex flex-col place-items-end">
    <div>
      <KwaiButton :href="`${website.url}/apps/auth/login`">
        Login
      </KwaiButton>
    </div>
  </div>
</template>
