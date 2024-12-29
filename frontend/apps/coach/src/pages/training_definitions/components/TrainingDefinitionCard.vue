<script setup lang="ts">
import { KwaiCard } from '@kwai/ui';
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
  <KwaiCard>
    <template #title>
      {{ trainingDefinition.name }}
    </template>
    <template #subtitle>
      {{ weekdayName }} {{ period }}
      <span v-if="trainingDefinition.team">
        &bull; {{ trainingDefinition.team.name }}
      </span>
    </template>
    {{ trainingDefinition.description }}
    <template #footer>
      <slot name="footer" />
    </template>
  </KwaiCard>
</template>

<style scoped>

</style>
