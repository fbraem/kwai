<script setup lang="ts">
// eslint-disable-next-line import/no-absolute-path
import trainingImage from '/training.jpg';
// eslint-disable-next-line import/no-absolute-path
import sporthalImage from '/sporthal.jpg';

import ApplicationList from '@root/components/ApplicationList.vue';
import LoadingIcon from '@root/components/icons/LoadingIcon.vue';
import { useTrainings } from '@root/composables/useTraining';
import type { TrainingPeriod } from '@root/composables/useTraining';
import type { Ref } from 'vue';
import { ref } from 'vue';
import { now } from '@kwai/date';

const period : Ref<TrainingPeriod> = ref({
  start: now(),
  end: now().add(1, 'week'),
});
const { isLoading, data: trainings } = useTrainings(period);
</script>

<template>
  <section>
    <div
      class="relative w-full bg-center bg-cover"
      :style="{ 'background-image' : `url(${trainingImage})` }"
    >
      <span class="absolute w-full h-full opacity-50 bg-gradient-to-br from-black to-red-600" />
      <div class="container relative mx-auto h-full p-4">
        <div class="grid lg:grid-cols-2 gap-10 justify-items-center lg:my-10">
          <div class="mx-auto">
            <img
              :src="sporthalImage"
              alt="sporthal"
              class="border-2 border-black max-h-80"
            >
          </div>
          <div class="flex flex-col gap-4">
            <ApplicationList :filter="['trainings']">
              <template
                #default="{ application }"
              >
                <h2 class="text-4xl font-semibold text-white mb-2">
                  {{ application.title }}
                </h2>
                <p
                  class="text-white leading-8"
                >
                  {{ application.short_description }}
                </p>
              </template>
            </ApplicationList>
            <div v-if="trainings">
              <div class="flex flex-row gap-4 items-center">
                <h3 class="text-white text-2xl font-semibold">
                  Volgende trainingen
                </h3>
                <div>
                  <LoadingIcon
                    v-show="isLoading"
                    class="w-8 h-8 fill-red-600 text-gray-600"
                  />
                </div>
              </div>
              <div class="bg-gray-100 px-3 py-2 text-gray-800 rounded divide-y divide-gray-300">
                <div
                  v-for="training in trainings.items.slice(0, 4)"
                  :key="training.id"
                  class="flex gap-4 py-1"
                >
                  <div class="text-sm text-center font-medium">
                    {{ training.start_date.format("DD-MM-YYYY HH:mm") }}&nbsp;-&nbsp;{{ training.end_date.format("HH:mm") }}
                  </div>
                  <div class="text-sm">
                    {{ training.title }}
                  </div>
                </div>
              </div>
            </div>
            <div class="my-6">
              <router-link
                class="border border-red-600 bg-red-600 hover:bg-white hover:text-red-600 rounded text-sm text-white py-1 px-3"
                :to="{ 'name': 'portal.trainings' }"
              >
                Alle trainingen
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
