<script setup lang="ts">
// eslint-disable-next-line import/no-absolute-path
import trainingImage from '/training.jpg';

import IntroSection from '@root/components/IntroSection.vue';
import { computed, ref, toRef, watch } from 'vue';
import type { Ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import { useApplications } from '@root/composables/useApplication';
import { usePages } from '@root/composables/usePage';
import { createDate, now } from '@kwai/date';
import type { TrainingPeriod } from '@root/composables/useTraining';
import { useTrainingDays, useTrainings } from '@root/composables/useTraining';
import TrainingTimeline from '@root/pages/trainings/components/TrainingTimeline.vue';
import SectionTitle from '@root/components/SectionTitle.vue';
import LeftArrowIcon from '@root/components/icons/LeftArrowIcon.vue';
import RightArrowIcon from '@root/components/icons/RightArrowIcon.vue';

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

// Trainings
const toDay = now();
const currentMonth = ref(toDay.month());
const currentYear = ref(toDay.year());

const route = useRoute();
const year: Ref<number> = ref(Number.parseInt(route.query.year as string ?? currentYear.value));
const month: Ref<number> = ref(Number.parseInt(route.query.month as string ?? currentMonth.value));
const trainingPeriod = computed<TrainingPeriod>(() => ({
  start: createDate(
    year.value,
    month.value
  ).startOf('month'),
  end: createDate(
    year.value,
    month.value
  ).endOf('month'),
}));

const { data: trainings } = useTrainings(toRef(trainingPeriod));

const trainingDays = ref({});
watch(trainings, (nv, ov) => {
  trainingDays.value = useTrainingDays(trainings?.value?.items || []);
});

const showPrevMonth = () => {
  if (month.value === 1) {
    month.value = 11;
    year.value = year.value - 1;
  } else {
    month.value = month.value - 1;
  }
};
const showCurrentMonth = () => {
  month.value = currentMonth.value;
  year.value = currentYear.value;
};
const showNextMonth = () => {
  if (month.value === 11) {
    month.value = 0;
    year.value = year.value + 1;
  } else {
    month.value = month.value + 1;
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
  <section
    id="trainings"
    class="py-12"
  >
    <div class="container mx-auto">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 divide-y divide-y-reverse md:divide-y-0 md:divide-x divide-gray-300">
        <div class="p-4 order-first md:col-span-2">
          <SectionTitle class="pb-4">
            Trainingsrooster
          </SectionTitle>
          <div class="flex gap-4 py-3">
            <button
              type="button"
              class="flex items-center focus:outline-none text-white bg-red-600 hover:bg-red-700 focus:ring-4 focus:ring-red-300 font-medium rounded text-sm px-3 py-1 dark:bg-red-500 dark:hover:bg-red-600 dark:focus:ring-red-800"
              @click="showPrevMonth"
            >
              <LeftArrowIcon class="w-4 h-4 mr-2 fill-current" /> Vorige Maand
            </button>
            <button
              type="button"
              class="flex items-center focus:outline-none text-white bg-red-600 hover:bg-red-700 focus:ring-4 focus:ring-red-300 font-medium rounded text-sm px-3 py-1 dark:bg-red-500 dark:hover:bg-red-600 dark:focus:ring-red-800"
              @click="showCurrentMonth"
            >
              Deze Maand
            </button>
            <button
              type="button"
              class="flex items-center focus:outline-none text-white bg-red-600 hover:bg-red-700 focus:ring-4 focus:ring-red-300 font-medium rounded text-sm px-3 py-1 dark:bg-red-500 dark:hover:bg-red-600 dark:focus:ring-red-800"
              @click="showNextMonth"
            >
              Volgende Maand <RightArrowIcon class="w-4 h-4 ml-2 fill-current" />
            </button>
          </div>
          <h3 class="text-2xl pb-4">
            {{ trainingPeriod.start.format("MMMM") }} {{ trainingPeriod.start.format("YYYY") }}
          </h3>
          <TrainingTimeline
            :training-days="trainingDays"
            class="text-gray-600"
          />
        </div>
      </div>
    </div>
  </section>
</template>
