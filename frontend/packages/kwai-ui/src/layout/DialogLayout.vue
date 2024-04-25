<template>
  <main class="w-full h-full">
    <div
      class="absolute top-0 w-full h-full bg-gray-900 bg-cover bg-center"
      :style="styles"
    >
      <div class="w-full h-full absolute opacity-60 bg-black" />
      <div class="flex flex-col content-center items-center justify-center h-full">
        <div class="w-auto px-8 relative">
          <router-view />
        </div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, StyleValue } from 'vue';
import type { Ref } from 'vue';

const props = defineProps<{
  image?: string
}>();

const styles: Ref<StyleValue[]> = ref([]);
if (props.image) {
  styles.value.push({ 'background-image': `url(${props.image}` });
}
</script>
