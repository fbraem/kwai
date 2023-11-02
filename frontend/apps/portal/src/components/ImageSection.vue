<script setup lang="ts">
interface Props {
  backgroundImage: string
}
defineProps<Props>();

</script>

<template>
  <section>
    <div
      class="relative w-full bg-center bg-cover"
      :style="{ 'background-image' : `url(${backgroundImage})` }"
    >
      <span class="absolute w-full h-full opacity-50 bg-gradient-to-br from-black to-red-600" />
      <slot />
    </div>
  </section>
</template>

<style scoped>

</style>
