<script setup lang="ts">
import { computed } from 'vue';
import {
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
} from '@kwai/ui';
import { useI18n } from 'vue-i18n';
import { useApplications } from '@root/composables/useApplication';
import PageForm from '@root/pages/pages/components/PageForm.vue';
import { usePage } from '@root/composables/usePageItem';

interface Props {
  id: string
}
const props = defineProps<Props>();

const { data: applications } = useApplications();

const enabled = computed(() => !!applications.value && !!id.value);
const id = computed(() => props.id);
const { data: page } = usePage(id, { enabled });

const { t } = useI18n({ useScope: 'global' });
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>{{ t('pages.edit.title') }}</ContainerSectionTitle>
    <ContainerSectionContent>
      <PageForm
        :page="page"
        :applications="applications"
      />
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
