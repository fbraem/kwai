<script setup lang="ts">
import AddMemberIcon from '@root/components/icons/AddMemberIcon.vue';
import { ContainerSection, ContainerSectionContent, KwaiButton } from '@kwai/ui';
import { useI18n } from 'vue-i18n';
import { computed } from 'vue';
const { t } = useI18n({ useScope: 'global' });

interface Props {
  id: string
}
const props = defineProps<Props>();

const id = computed(() => props.id);
</script>

<template>
  <ContainerSection>
    <ContainerSectionContent>
      <KwaiButton :to="{ name: 'club.teams.members.add', params: { id }}">
        <AddMemberIcon class="mr-2 w-4 fill-current" />
        {{ t('team.members.add') }}
      </KwaiButton>
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
