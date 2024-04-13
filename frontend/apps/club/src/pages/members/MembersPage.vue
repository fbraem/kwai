<script setup lang="ts">
import {
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
} from '@kwai/ui';
import { useMembers } from '@root/composables/useMember';
const { data: members } = useMembers({});
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>
      Leden
    </ContainerSectionTitle>
    <ContainerSectionContent>
      Beheer de leden...
      {{ members }}
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
