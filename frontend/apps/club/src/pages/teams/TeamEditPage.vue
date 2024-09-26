<script setup lang="ts">
import {
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
} from '@kwai/ui';
import TeamForm from '@root/pages/teams/components/TeamForm.vue';

import { useI18n } from 'vue-i18n';
import { computed } from 'vue';
import { useTeam } from '@root/composables/useTeam';
const { t } = useI18n({ useScope: 'global' });

interface Props {
  id: string
}
const props = defineProps<Props>();

const id = computed(() => props.id);
const { data: team } = useTeam(id);
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>{{ t('team.edit.title') }}</ContainerSectionTitle>
    <ContainerSectionContent>
      <TeamForm :team="team" />
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
