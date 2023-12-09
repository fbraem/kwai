<script setup lang="ts">
import { Card, CardTitle } from '@kwai/ui';
import type { TrainingDefinition } from '@root/composables/useTrainingDefinition';
import { computed } from 'vue';
import { weekday } from '@kwai/date';

interface Props {
  trainingDefinition: TrainingDefinition,
}
const props = defineProps<Props>();

const weekdayName = computed(() => weekday(props.trainingDefinition.weekday));
const period = computed(() => {
  return props.trainingDefinition.start_time.format('HH:mm') + ' - ' +
    props.trainingDefinition.end_time.format('HH:mm');
});
</script>

<template>
  <Card class="w-full">
    <template #header>
      <CardTitle class="p-3">
        <div class="font-bold text-lg text-gray-900">
          {{ trainingDefinition.name }}
        </div>
        <div class="text-sm text-gray-600">
          {{ weekdayName }} {{ period }}
          <span v-if="trainingDefinition.team">
            &bull; {{ trainingDefinition.team.name }}
          </span>
        </div>
      </CardTitle>
    </template>
    <p class="p-3">
      {{ trainingDefinition.description }}
    </p>
    <template #footer>
      <slot name="footer" />
    </template>
  </Card>
</template>

<style scoped>

</style>
