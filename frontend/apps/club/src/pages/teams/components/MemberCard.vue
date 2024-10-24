<script setup lang="ts">

import { KwaiBadge, KwaiButton, KwaiCard } from '@kwai/ui';
import type { TeamMember } from '@root/types/team';
import { computed } from 'vue';
import { now } from '@kwai/date';
import AddMemberIcon from '@root/components/icons/AddMemberIcon.vue';

interface Props {
  member: TeamMember
}
const props = defineProps<Props>();
const member = computed(() => props.member);
const validLicense = computed(() => {
  return !member.value.license.endDate.isBefore(now());
});
const age = computed(() => {
  return now().get('year') - member.value.birthdate.get('year');
});
const emit = defineEmits(['add']);
</script>

<template>
  <KwaiCard>
    <template #title>
      {{ member.lastName }} {{ member.firstName }}
    </template>
    <template #content>
      <div class="grid grid-cols-2">
        <div>Geboortedatum:</div>
        <div>{{ member.birthdate.format('L') }} ({{ age }})</div>
        <div>Licentie</div>
        <div>
          {{ member.license.number }} ({{ member.license.endDate.format('L') }})
          <KwaiBadge
            class="align-top"
            :severity="validLicense ? 'success' : 'danger'"
          />
        </div>
        <div>Nationaliteit:</div>
        <div>{{ member.nationality.iso3 }}</div>
      </div>
    </template>
    <template #footer>
      <div class="flex justify-end">
        <KwaiButton :method="() => emit('add')">
          <AddMemberIcon class="w-4 h-4 fill-primary-text" />
        </KwaiButton>
      </div>
    </template>
  </KwaiCard>
</template>

<style scoped>

</style>
