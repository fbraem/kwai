<script setup lang="ts">
// eslint-disable-next-line import/no-absolute-path
import sporthalImage from '/sporthal.jpg';

import ApplicationList from '@root/components/ApplicationList.vue';
import { useTrainings } from '@root/composables/useTraining';
import type { Training } from '@root/composables/useTraining';
import { computed, ref } from 'vue';
import { now } from '@kwai/date';
import ImageSection from '@root/components/ImageSection.vue';
import BetweenIcon from '@root/components/icons/BetweenIcon.vue';
import TrainingTimeline from '@root/pages/trainings/components/TrainingTimeline.vue';
import { getHeroImageUrl } from '@root/composables/useHeroImage';

const start = ref(now());
const end = ref(now().add(1, 'week'));
const { isLoading, data: trainings } = useTrainings({ start, end });

type TrainingDays = {[key: string] : Training[]};
const trainingDays = computed(() => {
  const result : TrainingDays = {};
  if (!trainings.value) {
    return {};
  }
  trainings.value.items.forEach(training => {
    const date = training.start_date.format('YYYY-MM-DD');
    if (!result[date]) {
      result[date] = [];
    }
    result[date].push(training);
  });
  return result;
});

const trainingImage = getHeroImageUrl('trainings');
</script>

<template>
  <ImageSection :background-image="trainingImage">
    <div class="flex flex-col items-center text-white pt-12 px-12">
      <ApplicationList :filter="['trainings']">
        <template
          #default="{ application }"
        >
          <h2 class="text-4xl font-bold mb-2">
            {{ application.title }}
          </h2>
        </template>
      </ApplicationList>
    </div>
    <div class="max-w-7xl mx-auto flex flex-wrap p-12">
      <div class="mb-12 w-full shrink-0 grow-0 basis-auto lg:mb-0 lg:w-5/12">
        <div class="flex lg:py-12">
          <img
            :src="sporthalImage"
            class="z-[10] w-full rounded-lg shadow-lg"
            alt="Sporthal"
          >
        </div>
      </div>
      <div class="w-full shrink-0 grow-0 basis-auto rounded-lg bg-zinc-50 opacity-75 lg:w-7/12 lg:ml-[-50px]">
        <div class="flex flex-col h-full p-6 lg:pl-12 lg:text-left">
          <h4 class="lg:ml-12 pb-2 text-2xl font-bold">
            Trainingsrooster
          </h4>
          <div
            v-if="!isLoading && Object.keys(trainingDays).length === 0"
            class="lg:ml-12 flex flex-row items-center flex-grow"
          >
            <div>
              <p>De komende dagen zijn er geen trainingen gepland.</p>
              <p>Wil je weten wanneer de volgende training is? Kijk dan op onze Training pagina.</p>
            </div>
          </div>
          <TrainingTimeline
            v-if="!isLoading && Object.keys(trainingDays).length > 0"
            :training-days="trainingDays"
            class="lg:ml-12"
          >
            <li
              v-for="(trainingDay, day) in trainingDays"
              :key="day"
            >
              <div class="flex-start flex items-center pt-3">
                <div class="-ml-[5px] mr-3 h-[9px] w-[9px] rounded-full bg-red-600" />
                <p class="font-bold">
                  {{ trainingDay[0].start_date.format("dddd") }} {{ trainingDay[0].start_date.format("DD-MM-YYYY") }}
                </p>
              </div>
              <div class="mb-6 ml-4 mt-2">
                <div
                  v-for="training in trainingDay"
                  :key="training.id"
                  class="flex items-center gap-4"
                >
                  <div>{{ training.start_date.format("HH:mm") }}u</div>
                  <BetweenIcon class="w-4 h-4" />
                  <div>{{ training.end_date.format("HH:mm") }}u</div>
                  <div class="font-medium">
                    {{ training.title }}
                  </div>
                </div>
              </div>
            </li>
          </TrainingTimeline>
          <div class="my-6 self-end">
            <router-link
              class="border border-red-600 bg-red-600 hover:bg-white hover:text-red-600 rounded text-sm text-white py-1 px-3"
              :to="{ 'name': 'portal.trainings' }"
            >
              Alle trainingen
            </router-link>
          </div>
          <div class="lg:ml-12 text-xs">
            Al onze trainingen gaan door in de gevechtssportzaal van de sporthal te Stekene.
          </div>
        </div>
      </div>
    </div>
  </ImageSection>
</template>
