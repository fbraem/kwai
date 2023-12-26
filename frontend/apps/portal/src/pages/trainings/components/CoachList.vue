<script setup lang="ts">
import { useCoaches } from '@root/composables/useCoach';

const { data: coaches } = useCoaches();
</script>

<template>
  <div class="bg-white">
    <div class="mx-auto grid max-w-7xl gap-x-8 gap-y-20 px-6 lg:px-8 xl:grid-cols-3">
      <div class="max-w-2xl">
        <h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
          Onze trainers
        </h2>
        <p class="mt-6 text-lg leading-8 text-gray-600">
          Onze trainersploeg is een gemotiveerd team bestaande uit gediplomeerde trainers. Alle trainers
          volgen jaarlijks bijscholingen zodat we steeds kwalitatieve trainingen kunnen aanbieden aan onze
          judoka's.
        </p>
      </div>
      <ul
        role="list"
        class="grid gap-x-8 gap-y-12 sm:grid-cols-2 sm:gap-y-16 xl:col-span-2"
      >
        <li
          v-for="coach in coaches"
          :key="coach.id"
        >
          <div class="flex items-center gap-x-6">
            <img
              class="h-16 w-16 rounded-full"
              src="no_avatar.png"
              alt=""
            >
            <div>
              <h3 class="text-base font-semibold leading-7 tracking-tight text-gray-900">
                {{ coach.name }}
              </h3>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>

</style>
