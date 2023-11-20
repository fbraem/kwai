<script setup lang="ts">
interface Props {
  url: string,
  logo: string
}
defineProps<Props>();
</script>

<template>
  <div>
    <a :href="url">
      <div class="flex flex-row items-center">
        <img
          :src="logo"
          class="w-16 mr-4"
          alt="logo"
        >
        <div class="sm:text-xl font-medium uppercase">
          <slot />
        </div>
      </div>
    </a>
  </div>
</template>

<style scoped>

</style>
