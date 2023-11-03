<script setup lang="ts">
interface Props {
  backgroundImage: string
}
defineProps<Props>();

</script>

<template>
  <section
    class="relative bg-center bg-cover"
    :style="{ 'background-image' : `url(${backgroundImage})` }"
  >
    <div class="bg-red-600/30 backdrop-brightness-75">
      <slot />
    </div>
  </section>
</template>

<style scoped>

</style>
