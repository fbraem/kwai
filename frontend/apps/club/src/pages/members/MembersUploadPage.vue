<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import {
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
  KwaiFileUpload,
  KwaiCheckbox,
} from '@kwai/ui';
import { type Ref, ref } from 'vue';
import { useHttpApi } from '@kwai/api';
import { MemberDocumentSchema, type Members } from '@root/composables/useMember';

const { t } = useI18n({ useScope: 'global' });

const useMemberUpload = (files: File[]) => {
  const members: Ref<Members|null> = ref(null);
  (async() => {
    const formData = new FormData();
    formData.append('member_file', files[0]);
    await useHttpApi()
      .url('/v1/club/members/upload')
      .body(formData)
      .post()
      .json()
      .then(json => {
        const result = MemberDocumentSchema.safeParse(json);
        if (result.success) {
          members.value = result.data as Members;
        } else {
          console.log(result.error);
          throw result.error;
        }
      })
    ;
  })();
  return members;
};

const members = ref();
const preview: Ref<boolean> = ref(true);

const upload = (files: File[]) => {
  members.value = useMemberUpload(files);
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
    <KwaiCheckbox v-model="preview">
      <template #label>
        Preview
      </template>
    </KwaiCheckbox>
    {{ members }}
  </ContainerSection>
</template>

<style scoped>

</style>
