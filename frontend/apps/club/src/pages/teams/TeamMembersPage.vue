<script setup lang="ts">
import {
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
  ErrorAlert,
  LoadingIcon,
  KwaiTable,
  KwaiTableColumn,
  KwaiTableCell, KwaiBadge,
} from '@kwai/ui';
import { computed } from 'vue';
import { useTeam } from '@root/composables/useTeam';
import { useI18n } from 'vue-i18n';
import { now } from '@kwai/date';

const { t } = useI18n({ useScope: 'global' });

interface Props {
  id: string
}
const props = defineProps<Props>();

const id = computed(() => props.id);
const { data: team, isPending, isError } = useTeam(id);

const year = now().year();
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle v-if="team">
      {{ t('team.members.title') }} {{ team.name }}
    </ContainerSectionTitle>
    <ContainerSectionContent>
      <div v-if="isPending">
        <LoadingIcon class="fill-primary-500 w-8 h-8 ml-2" />
      </div>
      <ErrorAlert v-else-if="isError">
        {{ t('teams.error') }}
      </ErrorAlert>
      <template v-else>
        <div v-if="team!.members.length === 0">
          {{ t('team.members.no_team_members') }}
        </div>
        <div
          v-else
          class="w-full"
        >
          <KwaiTable>
            <template #header>
              <KwaiTableColumn class="w-12" />
              <KwaiTableColumn>
                Naam
              </KwaiTableColumn>
              <KwaiTableColumn>
                Geboortedatum
              </KwaiTableColumn>
              <KwaiTableColumn>
                Licensie
              </KwaiTableColumn>
            </template>
            <template #body>
              <tr
                v-for="team_member in team!.members"
                :key="team_member.id"
              >
                <KwaiTableCell class="w-12" />
                <KwaiTableCell>
                  {{ team_member.lastName }} {{ team_member.firstName }}
                </KwaiTableCell>
                <KwaiTableCell>
                  {{ team_member.birthdate.format('L') }} ({{ year - team_member.birthdate.year() }})
                </KwaiTableCell>
                <KwaiTableCell class="inline-flex flex-col md:flex-row md:space-x-4">
                  <span>
                    {{ team_member.license.number }}
                  </span>
                  <span>
                    {{ team_member.license.endDate.format('L') }}
                    <KwaiBadge
                      class="align-top"
                      :severity="team_member.license.endDate.isBefore(now()) ? 'danger' : 'success'"
                    />
                  </span>
                </KwaiTableCell>
              </tr>
            </template>
          </KwaiTable>
        </div>
      </template>
    </ContainerSectionContent>
  </ContainerSection>
  <router-view />
</template>

<style scoped>

</style>
