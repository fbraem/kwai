<template>
  <div class="flex flex-col lg:flex-row flex-wrap">
    <div class="flex w-full sm:w-1/2">
      <div>
        {{ startHour }}u
      </div>
      <div class="mx-2">
        <i class="fas fa-arrows-alt-h" />
      </div>
      <div>
        {{ endHour }}u
      </div>
    </div>
    <div class="w-full md:w-1/2">
      <ul>
        <li
          v-for="team in training.teams"
          :key="team.id"
        >
          <div>{{ team.name }}</div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Training } from '@root/composables/useTraining';

interface Properties {
  training: Training
}
const props = defineProps<Properties>();

const startHour = props.training.start_date.format('HH:mm');
const endHour = props.training.end_date.format('HH:mm');
</script>
