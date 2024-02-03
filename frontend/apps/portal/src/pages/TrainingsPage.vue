<script setup lang="ts">
import IntroSection from '@root/components/IntroSection.vue';
import { computed, ref, toRef, watch } from 'vue';
import { useRouteQuery } from '@vueuse/router';
import { useRoute, useRouter } from 'vue-router';

import { useApplications } from '@root/composables/useApplication';
import { usePages } from '@root/composables/usePage';
import { createDate, now } from '@kwai/date';
import { useTrainingDays, useTrainings } from '@root/composables/useTraining';
import TrainingTimeline from '@root/pages/trainings/components/TrainingTimeline.vue';
import SectionTitle from '@root/components/SectionTitle.vue';
import LeftArrowIcon from '@root/components/icons/LeftArrowIcon.vue';
import RightArrowIcon from '@root/components/icons/RightArrowIcon.vue';
import PrimaryButton from '@root/components/PrimaryButton.vue';
import FullArticle from '@root/components/FullArticle.vue';
import CoachList from '@root/pages/trainings/components/CoachList.vue';

const route = useRoute();
const applicationName = route.meta.application as string;
const heroImageUrl = route.meta.heroImageUrl as string;

// Application
const { data: applications } = useApplications();
const application = computed(() => {
  if (applications.value) {
    return applications.value.find(application => application.name === applicationName);
  }
  return null;
});

// Pages
const { data: pages } = usePages(toRef(applicationName));
const sortedPages = computed(() => {
  return [...pages.value || []].sort((a, b) => b.priority - a.priority);
});
const articleSection = ref<HTMLInputElement | null>(null);
const currentPage = computed(() => {
  if (route.query.page) {
    if (articleSection.value) articleSection.value.scrollIntoView(true);
    return sortedPages.value.find(page => page.id === route.query.page);
  }
  return sortedPages.value[0];
});

const router = useRouter();
const gotoPage = (id: string) => {
  router.replace({ query: { ...route.query, page: id } });
  if (articleSection.value) articleSection.value.scrollIntoView(true);
};

// Trainings
const toDay = now();
const currentMonth = ref(toDay.month() + 1);
const currentYear = ref(toDay.year());

const year = useRouteQuery('year', currentYear.value, { transform: Number });
const month = useRouteQuery('month', currentMonth.value, { transform: Number });

const start = computed(() => createDate(year.value, month.value - 1, 1).startOf('month'));
const end = computed(() => createDate(year.value, month.value - 1, 1).endOf('month'));

const { data: trainings } = useTrainings({ start, end });

const trainingDays = ref({});
watch(trainings, (nv) => {
  if (!nv) {
    trainingDays.value = [];
  } else {
    trainingDays.value = useTrainingDays(nv.items || []);
  }
});

const showPrevMonth = () => {
  let prevMonth = month.value - 1;
  let prevYear = year.value;
  if (prevMonth < 1) {
    prevMonth = 12;
    prevYear -= 1;
  }
  router.replace({
    query: {
      ...route.query,
      year: prevYear,
      month: prevMonth,
    },
  });
};
const showCurrentMonth = () => {
  router.replace({
    query: {
      ...route.query,
      year: currentYear.value,
      month: currentMonth.value,
    },
  });
};
const showNextMonth = () => {
  let nextMonth = month.value + 1;
  let nextYear = year.value;
  if (nextMonth > 12) {
    nextMonth = 1;
    nextYear += 1;
  }
  router.replace({
    query: {
      ...route.query,
      year: nextYear,
      month: nextMonth,
    },
  });
};

</script>

<template>
  <IntroSection
    :hero-image-url="heroImageUrl"
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
      v-for="(page, index) in sortedPages"
      :key="page.id"
    >
      <a
        class="cursor-pointer"
        @click="gotoPage(page.id)"
      >
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
  <section
    id="trainings"
    class="py-12"
  >
    <div class="container mx-auto grid grid-cols-1 lg:grid-cols-2 gap-4">
      <div
        ref="articleSection"
        class="p-4 order-last lg:order-first"
      >
        <FullArticle
          v-if="currentPage"
          :page="currentPage"
        />
      </div>
      <div class="p-4 order-first lg:order-last">
        <SectionTitle class="pb-4">
          Trainingsrooster
        </SectionTitle>
        <div class="flex gap-4 py-3">
          <PrimaryButton
            :method="showPrevMonth"
            class="flex items-center"
          >
            <LeftArrowIcon class="w-4 h-4 mr-2 fill-current" /> Vorige Maand
          </PrimaryButton>
          <PrimaryButton
            :method="showCurrentMonth"
            class="flex items-center"
          >
            Deze Maand
          </PrimaryButton>
          <PrimaryButton
            :method="showNextMonth"
            class="flex items-center"
          >
            <RightArrowIcon class="w-4 h-4 mr-2 fill-current" /> Volgende Maand
          </PrimaryButton>
        </div>
        <h3 class="text-2xl pb-4">
          {{ start.format("MMMM") }} {{ start.format("YYYY") }}
        </h3>
        <TrainingTimeline
          :training-days="trainingDays"
          class="text-gray-600"
        />
      </div>
    </div>
  </section>
  <section id="coaches">
    <div class="container mx-auto">
      <CoachList />
    </div>
  </section>
</template>
