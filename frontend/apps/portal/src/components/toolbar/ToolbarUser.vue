<script setup lang="ts">
import { KwaiAuthenticateButton } from '@kwai/ui';
import {
  isLoggedIn, useHttpLogout,
} from '@kwai/api';

const logout = () => {
  useHttpLogout();
  window.location.reload();
};
</script>

<template>
  <div class="flex flex-col place-items-end">
    <KwaiAuthenticateButton
      :logged-in="isLoggedIn"
      :logout="logout"
    />
  </div>
</template>
