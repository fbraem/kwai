<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import {
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
  KwaiFileUpload,
} from '@kwai/ui';
import { useHttpApi } from '@kwai/api';

const { t } = useI18n({ useScope: 'global' });

const upload = (files: File[]) => {
  (async() => {
    const formData = new FormData();
    formData.append('member_file', files[0]);
    await useHttpApi()
      .url('/v1/club/members/upload')
      .body(formData)
      .post()
      .json((json) => console.log(json))
    ;
  })();
};
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>
      {{ t('members_upload.title') }}
    </ContainerSectionTitle>
    <ContainerSectionContent>
      {{ t('members_upload.description') }}
      <KwaiFileUpload
        name="test"
        :uploader="upload"
        :max-number-of-files="1"
      />
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
