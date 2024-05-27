<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import {
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
  KwaiFileUpload,
  KwaiCheckbox,
  ErrorAlert,
} from '@kwai/ui';
import { type Ref, ref } from 'vue';
import { useHttpApi, type JsonApiErrorType } from '@kwai/api';
import { MemberDocumentSchema, type Members, transform } from '@root/composables/useMember';

const { t } = useI18n({ useScope: 'global' });

const useMemberUpload = (files: File[]) => {
  (async() => {
    const formData = new FormData();
    formData.append('member_file', files[0]);
    await useHttpApi()
      .url('/v1/club/members/upload')
      .query({ preview: preview.value })
      .body(formData)
      .post()
      .json()
      .then(json => {
        const result = MemberDocumentSchema.safeParse(json);
        if (result.success) {
          errors.value = result.data.errors ?? [];
          count.value = result.data.meta?.count ?? 0;
          members.value = transform(result.data) as Members;
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
const errors: Ref<JsonApiErrorType[]> = ref([]);
const count = ref(0);

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
      <div>
        {{ t('members_upload.description') }}
      </div>
      <div class="w-full flex items-center space-x-5">
        <div class="w-2/3">
          <KwaiFileUpload
            name="test"
            :uploader="upload"
            :max-number-of-files="1"
          />
        </div>
        <div class="w-1/3 flex flex-col items-center">
          <p class="text-sm">
            {{ t('members_upload.preview_description') }}
          </p>
          <KwaiCheckbox v-model="preview">
            <template #label>
              {{ t('members_upload.preview') }}
            </template>
          </KwaiCheckbox>
        </div>
      </div>
    </ContainerSectionContent>
  </ContainerSection>
  <ContainerSection v-if="errors.length > 0">
    <ContainerSectionContent>
      <ErrorAlert>
        {{ t('members_upload.error.message') }}
      </ErrorAlert>
      <table class="divide-y divide-gray-400 w-full rounded-lg">
        <thead>
          <tr>
            <th class="w-1/6 px-6 py-3 text-left text-sm uppercase">
              {{ t('members_upload.error.row') }}
            </th>
            <th class="px-6 py-3 text-left text-sm uppercase">
              {{ t('members_upload.error.description') }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="error in errors"
            :key="error.source!.pointer"
          >
            <th class="w-1/6 px-6 py-3 text-left">
              {{ error.source!.pointer }}
            </th>
            <td class="px-6 py-3 text-left">
              {{ error.detail }}
            </td>
          </tr>
        </tbody>
      </table>
    </ContainerSectionContent>
  </ContainerSection>
  <ContainerSection v-if="members && members.items">
    <ContainerSectionContent>
      <div>
        <p>
          Er zijn {{ members.meta.count }} leden gevonden in dit bestand.
        </p>
      </div>
      <table
        v-if="members && members.items"
        class="divide-y divide-gray-400 w-full rounded-lg"
      >
        <thead>
          <tr>
            <th class="w-1/6 px-6 py-3 text-left text-sm uppercase">
              {{ t('members_upload.error.row') }}
            </th>
            <th class="px-6 py-3 text-left text-sm uppercase">
              {{ t('members_upload.error.description') }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(member, index) in members.items"
            :key="index"
          >
            <th class="w-1/6 px-6 py-1 text-left">
              {{ index + 1 }}
            </th>
            <td class="px-6 py-1 text-left">
              {{ member.person.lastName }} {{ member.person.firstName }}
            </td>
          </tr>
        </tbody>
      </table>
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
