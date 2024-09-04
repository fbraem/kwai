<script setup lang="ts">
import { useTeams } from '@root/composables/useTeam';
import { useI18n } from 'vue-i18n';
import {
  ContainerSection,
  ContainerSectionTitle,
  ContainerSectionContent,
  ErrorAlert,
  LoadingIcon,
  CheckIcon,
  CancelIcon,
} from '@kwai/ui';

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
          class="fill-primary-500 w-8 h-8 ml-2"
        />
      </div>
      <ErrorAlert v-else-if="isError">
        {{ t('teams.error') }}
      </ErrorAlert>
      <table
        v-else-if="teams"
        class="w-full text-sm text-left"
      >
        <thead class="text-xs text-gray-700 uppercase bg-gray-50">
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
              class="px-6 py-3"
            >
              {{ t('teams.remark') }}
            </th>
          </tr>
        </thead>
        <tbody>
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
            <td class="px-6 py-4">
              {{ team.remark }}
            </td>
          </tr>
        </tbody>
      </table>
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
