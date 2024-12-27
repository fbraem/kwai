<template>
  <IntroSection :hero-image-url="heroImage">
    <div class="container lg:max-w-5xl relative mx-auto h-full flex items-center">
      <div class="max-w-md flex flex-col space-y-5 p-4">
        <h1 class="text-4xl font-semibold text-white">
          {{ title }}
        </h1>
        <template
          v-for="(text, index) in portal.promotion"
          :key="index"
        >
          <p class="text-white leading-8 text-xl">
            {{ text }}
          </p>
        </template>
      </div>
    </div>
  </IntroSection>
  <HomeSectionApplications :applications="listedApplications" />
  <HomeSectionNews />
  <HomeSectionTrainings />
  <HomeSectionClub />
</template>

<script setup lang="ts">
import type { ShallowReactive } from 'vue';
import { shallowReactive } from 'vue';

import ClubIcon from '@theme/icons/ClubIcon.vue';
import NewsIcon from '@theme/icons/NewsIcon.vue';
import TrainingIcon from '@theme/icons/TrainingIcon.vue';

import { portal, website } from '@kwai/config';
import IntroSection from '@root/components/IntroSection.vue';
import HomeSectionApplications from '@root/components/home/HomeSectionApplications.vue';
import HomeSectionNews from '@root/components/home/HomeSectionNews.vue';
import HomeSectionTrainings from '@root/components/home/HomeSectionTrainings.vue';
import HomeSectionClub from '@root/components/home/HomeSectionClub.vue';
import { heroImage } from '@root/composables/useHeroImage';
import { useTitle } from '@vueuse/core';

interface ListedApplications {
  [key: string]: ShallowReactive<any>
}

const title = useTitle();

const listedApplications: ListedApplications = shallowReactive({
  club: ClubIcon,
  news: NewsIcon,
  trainings: TrainingIcon,
});
</script>
