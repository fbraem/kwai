<script setup lang="ts">
import { computed, type Ref, toRef } from 'vue';
import {
  ContainerSection,
  ContainerSectionTitle,
  ContainerSectionContent,
  ErrorAlert,
  KwaiCheckboxField,
  KwaiInputField,
  KwaiPanel,
  LoadingIcon,
} from '@kwai/ui';
import MemberCard from '@root/pages/teams/components/MemberCard.vue';
import { useI18n } from 'vue-i18n';
import { useField, useForm } from 'vee-validate';
import { now } from '@kwai/date';
import {
  type TeamFilter, type TeamMemberData,
  useAddTeamMemberMutation,
  useTeamMembers, useUpdateTeamMemberCache,
} from '@root/composables/useTeamMember';
import type { TeamMember } from '@root/types/team';

interface Props {
  id: string
}
const props = defineProps<Props>();

const id = toRef(props.id);

const teamFilter: Ref<TeamFilter> = toRef({
  id: id.value,
  inTeam: false,
});

const { t } = useI18n({ useScope: 'global' });
const { data: members, isPending, isError } = useTeamMembers({ team: teamFilter });

interface FilterForm {
  name: string,
  age?: number,
  validLicense: boolean,
}
useForm<FilterForm>({
  initialValues: {
    name: '',
    validLicense: true,
  },
});

const { value: filterNameFieldValue } = useField<string>('name');
const { value: filterAgeFieldValue } = useField<number>('age');
const { value: filterValidLicenseFieldValue } = useField<boolean>('validLicense');

const filteredMembers = computed(() => {
  if (members.value) {
    let result = members.value.items;
    if (filterValidLicenseFieldValue.value) {
      result = result.filter((m: TeamMember) => !m.license.endDate.isBefore(now()));
    }
    if (filterAgeFieldValue.value) {
      result = result.filter(
        (m: TeamMember) => (now().get('year') - m.birthdate.get('year')) === Number(filterAgeFieldValue.value)
      );
    }
    if (filterNameFieldValue.value) {
      result = result.filter(
        (m: TeamMember) => (m.lastName + ' ' + m.firstName).toLowerCase().includes(filterNameFieldValue.value.toLocaleLowerCase())
      );
    }
    return result;
  }
  return [];
});
const updateTeamMemberCache = useUpdateTeamMemberCache();
const { mutate: mutateAddTeamMember } = useAddTeamMemberMutation({
  onSuccess: (data: TeamMember, variables: TeamMemberData) => {
    // On success, remove the member from the list.
    updateTeamMemberCache(data, variables);
  },
});
const addMemberToTeam = (teamMember: TeamMember) => {
  mutateAddTeamMember({
    team_id: id.value,
    member: {
      data: {
        type: 'team_members',
        id: teamMember.id,
        attributes: {
          active: true,
          first_name: teamMember.firstName,
          last_name: teamMember.lastName,
          license_number: teamMember.license.number,
          license_end_date: teamMember.license.endDate.format(),
          gender: teamMember.gender,
          birthdate: teamMember.birthdate.format(),
          active_in_club: teamMember.activeInClub,
        },
        relationships: {
          nationality: {
            data: {
              type: 'countries',
              id: teamMember.nationality.id,
            },
          },
        },
      },
      included: [],
    },
  });
};
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>{{ t('team.member_add.title') }}</ContainerSectionTitle>
    <ContainerSectionContent>
      <div v-if="isPending">
        <LoadingIcon class="fill-primary-500 w-8 h-8" />
      </div>
      <ErrorAlert v-else-if="isError">
        {{ t('teams.error') }}
      </ErrorAlert>
      <template v-else>
        <div v-if="members!.meta.count === 0">
          {{ t('team.members.no_members') }}
        </div>
        <div v-else>
          <KwaiPanel class="mb-4">
            <template #header>
              <span class="font-bold">{{ t('team.member_add.filter.title') }}</span>
            </template>
            <div class="flex flex-col md:flex-row md:place-items-end gap-4">
              <div>
                <KwaiInputField name="name">
                  <template #label>
                    {{ t('team.member_add.filter.name') }}
                  </template>
                </KwaiInputField>
              </div>
              <div>
                <KwaiInputField name="age">
                  <template #label>
                    {{ t('team.member_add.filter.age') }}
                  </template>
                </KwaiInputField>
              </div>
              <div>
                <KwaiCheckboxField name="validLicense">
                  <template #label>
                    {{ t('team.member_add.filter.valid_license') }}
                  </template>
                </KwaiCheckboxField>
              </div>
            </div>
          </KwaiPanel>
          <p class="mb-2 text-sm text-gray-600">
            {{ t('team.member_add.filter.number_of_members', filteredMembers.length ) }}
          </p>
          <div
            class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4"
          >
            <MemberCard
              v-for="member in filteredMembers"
              :key="member.id"
              class="bg-green-100"
              :member="member"
              @add="addMemberToTeam(member)"
            />
          </div>
        </div>
      </template>
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
