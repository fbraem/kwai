<template>
  <IntroSection
    :hero-image-url="newsHeroImage"
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
  <div class="bg-zinc-50">
    <router-view />
  </div>
</template>

<script setup lang="ts">
import IntroSection from '@root/components/IntroSection.vue';
// eslint-disable-next-line import/no-absolute-path
import newsHeroImage from '/news.jpg';
</script>
