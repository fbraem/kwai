<template>
  <tr>
    <td class="text-left px-6 py-3">
      <div class="font-semibold">
        {{ nameOfDay }}
      </div>
      <div class="text-sm">
        {{ formattedDay }}
      </div>
    </td>
    <td class="pl-6">
      <div class="divide-y divide-y-1 divide-gray-400 w-full">
        <div
          v-for="training in trainings"
          :key="training.id"
          class="py-3"
        >
          <TrainingPeriod :training="training" />
        </div>
      </div>
    </td>
  </tr>
</template>

<script setup lang="ts">
import TrainingPeriod from '@root/pages/trainings/components/TrainingPeriod.vue';
import type { Training } from '@root/stores/trainingStore';
import { createDate } from '@kwai/date';
import { computed, ref } from 'vue';

interface Properties {
  day: string,
  trainings: Training[]
}
const props = defineProps<Properties>();

const day = ref(createDate(props.day));
const formattedDay = computed(() => day.value.format('L'));
const nameOfDay = computed(() => day.value.format('dddd'));
</script>
