<template>
  <section>
    <div
      class="relative"
      :style="{ 'height': `${height}px` }"
    >
      <div
        class="absolute w-full h-full bg-center xl:bg-top bg-cover"
        :style="{ 'background-image': 'url(' + heroImageUrl + ')' }"
      >
        <span class="w-full h-full absolute opacity-50 bg-gradient-to-br from-black to-red-600" />
        <slot />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
interface Props {
  heroImageUrl: string,
  height?: number,
}

withDefaults(
  defineProps<Props>(),
  {
    height: 500,
  }
);
</script>
