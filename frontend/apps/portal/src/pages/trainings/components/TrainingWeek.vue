<template>
  <div class="flex justify-between gap-4 mb-3">
    <div>
      <a
        class="border border-red-600 bg-red-600 hover:cursor-pointer hover:bg-white hover:text-red-600 text-white rounded-full py-1.5 px-3 text-xs uppercase mr-1 mb-1 inline-flex items-center"
        @click="prev()"
      >
        <PrevIcon class="mr-1 w-4 h-4 fill-current" /> Vorige Periode
      </a>
    </div>
    <div>
      <a
        class="border border-red-600 bg-red-600 hover:cursor-pointer hover:bg-white hover:text-red-600 text-white rounded-full py-1.5 px-3 text-xs uppercase mr-1 mb-1 inline-flex items-center"
        @click="today()"
      >
        Vandaag
      </a>
    </div>
    <div>
      <a
        class="border border-red-600 bg-red-600 hover:cursor-pointer hover:bg-white hover:text-red-600 text-white rounded-full py-1.5 px-3 text-xs uppercase mr-1 mb-1 inline-flex items-center"
        @click="next()"
      >
        Volgende Periode
        <NextIcon class="ml-1 w-4 h-4 fill-current" />
      </a>
    </div>
  </div>
  <div class="text-xs text-gray-800 text-center">
    Trainingen van
    <span class="font-semibold">{{ period.start.format('DD-MM-YYYY') }}</span>
    tot <span class="font-semibold">{{ period.end.format('DD-MM-YYYY') }}</span>
  </div>
  <div
    v-if="!loading && trainings.length === 0"
    class="text-center border bg-red-100 border-red-600 px-3 py-2 text-sm my-6"
  >
    Er zijn geen trainingen voor deze periode
  </div>
  <div
    v-else
    class="my-6"
  >
    <table class="divide-y divide-gray-400 w-full bg-gray-200 rounded-lg mb-3">
      <thead>
        <tr>
          <th class="w-1/3 px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Datum
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Tijdstip
          </th>
        </tr>
      </thead>
      <template
        v-for="(trainingsOnThisDay, day) in trainingDays"
        :key="day"
      >
        <TrainingDay
          :day="day"
          :trainings="trainingsOnThisDay"
        />
      </template>
    </table>
  </div>
</template>

<script setup lang="ts">
import type { Training } from '@root/stores/trainingStore';
import { useTrainingStore } from '@root/stores/trainingStore';
import { computed } from 'vue';
import PrevIcon from '@root/components/icons/PrevIcon.vue';
import NextIcon from '@root/components/icons/NextIcon.vue';
import TrainingDay from '@root/pages/trainings/components/TrainingDay.vue';

const store = useTrainingStore();

const period = computed(() => store.period);

const prev = () => store.changePeriod(-1);
const next = () => store.changePeriod(1);
const today = () => store.resetPeriod();

const trainings = computed(() => store.trainings);
const { loading } = store.load();

const trainingDays = computed(() => {
  const days: { [key:string]: Training[] } = {};
  trainings.value.forEach((t) => {
    const date = t.start_date.format('YYYY-MM-DD');
    if (!days[date]) {
      days[date] = [];
    }
    days[date].push(t);
  });
  return days;
});
</script>
