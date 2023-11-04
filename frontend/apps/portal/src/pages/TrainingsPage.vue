<script setup lang="ts">
// eslint-disable-next-line import/no-absolute-path
import trainingImage from '/training.jpg';

import IntroSection from '@root/components/IntroSection.vue';
import { computed } from 'vue';
import { useRouter } from 'vue-router';

import { useApplications } from '@root/composables/useApplication';
import { usePages } from '@root/composables/usePage';

// Application
const { data: applications } = useApplications();
const application = computed(() => {
  if (applications.value) {
    return applications.value.find(application => application.name === 'trainings');
  }
  return null;
});
const applicationName = computed(() => {
  return application.value?.name || '';
});

// Pages
const { data: pages } = usePages(applicationName);

const router = useRouter();
const gotoPage = async(id: string) => {
  await router.push({
    name: 'portal.trainings.article',
    params: { id },
  });
  const el = document.querySelector('#article');
  if (el) {
    el.scrollIntoView({ block: 'center' });
  }
};
</script>

<template>
  <IntroSection
    :hero-image-url="trainingImage"
    :height="300"
  >
    <div class="container lg:max-w-5xl relative mx-auto flex h-full items-center">
      <div
        v-if="application"
        class="flex flex-col space-y-5 p-4"
      >
        <h1 class="text-4xl font-semibold text-white">
          {{ application.title }}
        </h1>
        <p
          class="text-white leading-8 text-xl"
        >
          {{ application.short_description }}
        </p>
      </div>
    </div>
  </IntroSection>
  <section class="grid grid-flow-col auto-cols-fr">
    <template
      v-for="(page, index) in pages"
      :key="page.id"
    >
      <a @click="gotoPage(page.id)">
        <div
          class="text-center text-white p-8 h-full"
          :class="{ 'bg-black' : index % 2, 'bg-red-600': !(index % 2) }"
        >
          <h2 class="text-2xl mb-2 font-medium">
            {{ page.texts[0].title }}
          </h2>
          <div
            class="text-gray-200"
            v-html="page.texts[0].summary"
          />
        </div>
      </a>
    </template>
  </section>
  <div id="article" />
  <router-view />
  <section class="py-24">
    <div class="container mx-auto">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 divide-y divide-y-reverse md:divide-y-0 md:divide-x divide-gray-300">
        <div class="p-4 order-first md:order-last">
          <h2 class="text-center text-4xl mb-2">
            Agenda
          </h2>
          <p class="text-center text-xs text-gray-500 mb-8">
            Een overzicht van de trainingen tijdens deze periode
          </p>
          <div />
        </div>
      </div>
    </div>
  </section>
</template>
