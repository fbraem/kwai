<script setup lang="ts">
import { useTeams } from '@root/composables/useTeam';
import { useI18n } from 'vue-i18n';
import {
  ContainerSection,
  ContainerSectionTitle,
  ContainerSectionContent,
  ErrorAlert,
  KwaiButton,
  LoadingIcon,
  CheckIcon,
  CancelIcon,
  EditIcon,
} from '@kwai/ui';
import MemberIcon from '@root/components/icons/MemberIcon.vue';

const { t } = useI18n({ useScope: 'global' });
const { data: teams, isPending, isError } = useTeams({});
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>
      {{ t('teams.title') }}
    </ContainerSectionTitle>
    <ContainerSectionContent>
      <div v-if="isPending">
        <LoadingIcon
          class="fill-primary-500 w-8 h-8"
        />
      </div>
      <ErrorAlert v-else-if="isError">
        {{ t('teams.error') }}
      </ErrorAlert>
      <table
        v-else-if="teams"
        class="w-full text-sm text-left"
      >
        <thead class="text-xs text-gray-700 uppercase bg-primary-100">
          <tr>
            <th
              scope="col"
              class="px-6 py-3 w-10"
            />
            <th
              scope="col"
              class="px-6 py-3"
            >
              {{ t('teams.name') }}
            </th>
            <th
              scope="col"
              class="px-6 py-3 text-center"
            >
              {{ t('teams.members') }}
            </th>
            <th
              scope="col"
              class="px-6 py-3"
            >
              {{ t('teams.remark') }}
            </th>
            <th />
          </tr>
        </thead>
        <tbody class="divide-y divide-primary-100">
          <tr
            v-for="team in teams.items"
            :key="team.id"
          >
            <td class="px-6 py-4">
              <CheckIcon
                v-if="team.active"
                class="w-4 fill-green-600 font-bold"
              />
              <CancelIcon
                v-else
                class="w-4 fill-red-500 font-bold"
              />
            </td>
            <td class="px-6 py-4">
              {{ team.name }}
            </td>
            <td class="px-6 py-4 text-center">
              {{ team.members.length }}
            </td>
            <td class="px-6 py-4">
              {{ team.remark }}
            </td>
            <td class="px-6 py-4 flex flex-col space-y-1 sm:flex-row sm:space-y-0 sm:space-x-1 sm:justify-end">
              <KwaiButton
                :to="{name: 'club.teams.edit', params: { id: team.id }}"
                class="w-12"
              >
                <template #icon>
                  <EditIcon class="w-4 fill-current" />
                </template>
              </KwaiButton>
              <KwaiButton
                :to="{name: 'club.teams.members', params: { id: team.id }}"
                class="w-12"
              >
                <template #icon>
                  <MemberIcon class="w-4 fill-current" />
                </template>
              </KwaiButton>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="w-full flex flex-col items-end">
        <KwaiButton :to="{name: 'club.teams.create'}">
          Nieuw Team
        </KwaiButton>
      </div>
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
