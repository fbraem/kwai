<script setup lang="ts">
import {
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
} from '@kwai/ui';
import { type Member, useMembers } from '@root/composables/useMember';
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import { breakpointsTailwind, useBreakpoints } from '@vueuse/core';

const breakpoints = useBreakpoints(breakpointsTailwind);
const largerThanLg = breakpoints.greater('lg');

const { t } = useI18n({ useScope: 'global' });

const { data: members } = useMembers({});
const sortedMembers = computed(() => {
  const result: Record<string, Member[]> = {};
  if (!members.value) return result;
  members.value.items.forEach(member => {
    const firstChar = member.person.lastName.charAt(0).toUpperCase();
    if (!result[firstChar]) result[firstChar] = [];
    result[firstChar].push(member);
  });
  for (const letter in result) {
    result[letter].sort((a, b) => {
      const aName = a.person.lastName + a.person.firstName;
      const bName = b.person.lastName + b.person.firstName;
      if (aName < bName) return -1;
      if (aName > bName) return 1;
      return 0;
    });
  }
  return result;
});
const memberLetters = computed(() => {
  return Object.keys(sortedMembers.value).sort();
});
const alphabet = [...Array(26)].map((_, i) => String.fromCharCode(65 + i));
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>
      {{ t('members.title') }}
    </ContainerSectionTitle>
    <ContainerSectionContent>
      <x-button-group v-if="largerThanLg">
        <x-button
          v-for="letter in alphabet"
          :key="letter"
          size="xs"
          color="primary"
          class="px-3"
        >
          {{ letter }}
        </x-button>
      </x-button-group>
      <div
        v-else
        class="flex flex-col items-center"
      >
        <x-button-group>
          <x-button
            v-for="n in 13"
            :key="n"
            size="xs"
            color="primary"
            class="px-3"
          >
            {{ alphabet[n-1] }}
          </x-button>
        </x-button-group>
        <x-button-group>
          <x-button
            v-for="n in 13"
            :key="n"
            size="xs"
            color="primary"
            class="px-3"
          >
            {{ alphabet[n+12] }}
          </x-button>
        </x-button-group>
      </div>
      <ul class="columns-3xs w-2/3 mx-auto">
        <li
          v-for="letter in memberLetters"
          :key="letter"
        >
          <h2 class="text-2xl font-extrabold py-2">
            {{ letter }}
          </h2>
          <ul>
            <li
              v-for="member in sortedMembers[letter]"
              :key="member.id"
            >
              {{ member.person.lastName }} {{ member.person.firstName }}
            </li>
          </ul>
        </li>
      </ul>
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
