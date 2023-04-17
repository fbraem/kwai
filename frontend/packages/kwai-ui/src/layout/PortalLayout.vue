<template>
  <div class="flex h-screen">
    <router-view name="sidebar" />
    <div class="flex-1 flex flex-col">
      <router-view name="toolbar" />
      <main
        id="main"
        class="flex-1"
      >
        <router-view name="main" />
        <router-view name="footer" />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>
