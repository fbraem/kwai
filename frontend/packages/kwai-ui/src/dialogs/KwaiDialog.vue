<script setup lang="ts"></script>

<template>
  <div class="relative z-10">
    <div
      class="fixed inset-0 bg-gray-500/75"
      aria-hidden="true"
    />
    <div class="fixed inset-0 z-10 w-screen overflow-y-auto">
      <div
        class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0"
      >
        <div
          class="relative overflow-hidden rounded-lg shadow-xl sm:my-8 sm:w-full sm:max-w-lg"
        >
          <slot />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
