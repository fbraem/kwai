<script setup lang="ts">
import {
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
  KwaiButton,
  KwaiButtonGroup,
} from '@kwai/ui';
import { useMembers } from '@root/composables/useMember';
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import { breakpointsTailwind, useBreakpoints } from '@vueuse/core';
import type { Member } from '@root/types/member';

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
      <span v-if="members">
        {{ t('members.count', { count: members.meta.count }) }}
      </span>
      <KwaiButtonGroup
        v-if="largerThanLg"
      >
        <KwaiButton
          v-for="letter in alphabet"
          :key="letter"
          class="bg-primary-500 text-primary-text"
          small
          :href="`#a_member_${letter}`"
        >
          {{ letter }}
        </KwaiButton>
      </KwaiButtonGroup>
      <div
        v-else
        class="flex flex-col items-center"
      >
        <KwaiButtonGroup>
          <KwaiButton
            v-for="n in 13"
            :key="n"
            class="bg-primary-500 text-primary-text"
            small
            :href="`#a_member_${alphabet[n-1]}`"
          >
            {{ alphabet[n-1] }}
          </KwaiButton>
        </KwaiButtonGroup>
        <KwaiButtonGroup>
          <KwaiButton
            v-for="n in 13"
            :key="n"
            class="bg-primary-500 text-primary-text"
            small
            :href="`#a_member_${alphabet[n+12]}`"
          >
            {{ alphabet[n+12] }}
          </KwaiButton>
        </KwaiButtonGroup>
      </div>
      <ul class="columns-3xs w-2/3 mx-auto">
        <li
          v-for="letter in memberLetters"
          :key="letter"
        >
          <a :id="`a_member_${letter}`" />
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
