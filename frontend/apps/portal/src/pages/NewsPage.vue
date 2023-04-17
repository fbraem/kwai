<template>
  <IntroSection
    :hero-image-url="newsHeroImage"
    :height="300"
  >
    <div class="container lg:max-w-5xl relative mx-auto flex h-full items-center">
      <div class="flex flex-col space-y-5 p-4">
        <h1 class="text-4xl font-semibold text-white">
          Nieuws
        </h1>
        <p class="text-white leading-8 text-xl">
          Op deze pagina vind je al het nieuws van onze club.
        </p>
      </div>
    </div>
  </IntroSection>
</template>

<script setup lang="ts">
import IntroSection from '@root/components/IntroSection.vue';
// eslint-disable-next-line import/no-absolute-path
import newsHeroImage from '/news.jpg';
</script>
