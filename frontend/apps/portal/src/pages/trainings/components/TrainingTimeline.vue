<script setup lang="ts">
import type { TrainingDays } from '@root/composables/useTraining';
import BetweenIcon from '@root/components/icons/BetweenIcon.vue';
import { KwaiTag } from '@kwai/ui';

interface Props {
  trainingDays: TrainingDays
}
defineProps<Props>();
</script>

<template>
  <ol class="border-l border-red-600">
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
          :class="{ 'cancelled' : training.cancelled }"
        >
          <div>{{ training.start_date.format("HH:mm") }}u</div>
          <BetweenIcon class="w-4 h-4" />
          <div>{{ training.end_date.format("HH:mm") }}u</div>
          <div class="font-medium">
            {{ training.title }}
          </div>
          <div v-if="training.cancelled">
            <KwaiTag>
              Geannuleerd
            </KwaiTag>
          </div>
        </div>
      </div>
    </li>
  </ol>
</template>

<style scoped>
.cancelled {
  @apply line-through decoration-red-600 decoration-2 text-gray-400;
}
</style>
