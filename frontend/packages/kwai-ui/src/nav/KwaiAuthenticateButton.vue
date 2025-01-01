<script setup lang="ts">
import { KwaiButton } from '../form';
import {
  LoginIcon, LogoutIcon,
} from '../icons';

interface Props {
  loggedIn: boolean
  logout: () => void
}
defineProps<Props>();
</script>

<template>
  <div v-if="loggedIn">
    <KwaiButton
      :method="logout"
      small
    >
      <template #icon>
        <LogoutIcon class="w-4 fill-current" />
      </template>
    </KwaiButton>
  </div>
  <div v-else>
    <KwaiButton
      href="/apps/auth/login"
      small
    >
      <template #icon>
        <LoginIcon class="w-4 fill-current" />
      </template>
    </KwaiButton>
  </div>
</template>

<style scoped>
</style>
