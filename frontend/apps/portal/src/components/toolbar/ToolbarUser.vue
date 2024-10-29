<script setup lang="ts">
import { website } from '@kwai/config';
import { KwaiButton } from '@kwai/ui';
import { isLoggedIn, useHttpLogout } from '@kwai/api';

const loggedIn = isLoggedIn;
const logout = () => {
  useHttpLogout();
  window.location.reload();
};
</script>

<template>
  <div class="flex flex-col place-items-end">
    <div v-if="loggedIn">
      <KwaiButton :method="logout">
        Logout
      </KwaiButton>
    </div>
    <div v-else>
      <KwaiButton :href="`${website.url}/apps/auth/login`">
        Login
      </KwaiButton>
    </div>
  </div>
</template>
