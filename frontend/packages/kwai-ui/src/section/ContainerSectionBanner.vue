<script setup lang="ts">
</script>

<template>
  <div class="w-full max-w-screen-xl mx-auto">
    <div class="relative overflow-hidden bg-white shadow-md sm:rounded-lg">
      <div class="flex-row items-center p-4 space-y-3 sm:flex sm:space-y-0 sm:space-x-4">
        <div class="flex-grow">
          <slot name="left" />
        </div>
        <div>
          <slot name="right" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
