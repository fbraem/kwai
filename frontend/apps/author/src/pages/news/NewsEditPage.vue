<script setup lang="ts">
import { useNewsItem } from '@root/composables/useNewsItem';
import { computed } from 'vue';
import {
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
} from '@kwai/ui';
import { useI18n } from 'vue-i18n';
import { useApplications } from '@root/composables/useApplication';
import NewsForm from '@root/pages/news/components/NewsForm.vue';

interface Props {
  id: string
}
const props = defineProps<Props>();

const { data: applications } = useApplications();

const enabled = computed(() => !!applications.value && !!id.value);
const id = computed(() => props.id);
const { data: newsItem } = useNewsItem(id, { enabled });

const { t } = useI18n({ useScope: 'global' });
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>{{ t('news.edit.title') }}</ContainerSectionTitle>
    <ContainerSectionContent>
      <NewsForm
        :news-item="newsItem"
        :applications="applications"
      />
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
