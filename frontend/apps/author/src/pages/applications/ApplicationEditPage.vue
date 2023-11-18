<script setup lang="ts">
import { Button, ContainerSection, ContainerSectionContent, ContainerSectionTitle, InputField, TextareaField } from '@kwai/ui';
import { useApplication, useApplicationMutation } from '@root/composables/useApplication';
import type { Application } from '@root/composables/useApplication';
import { useForm } from 'vee-validate';
import { useI18n } from 'vue-i18n';
import { computed, ref, watch } from 'vue';
import type { Ref } from 'vue';

interface Props {
  id: string
}
const props = defineProps<Props>();

const { t } = useI18n({ useScope: 'global' });

function isRequired(value: string): string|boolean {
  if (value && value.trim()) {
    return true;
  }
  return t('applications.edit.form.required');
}

const { handleSubmit, setValues } = useForm({
  validationSchema: {
    title: isRequired,
  },
});

const id = computed(() => props.id);

const { data: application } = useApplication(id);

watch(application, nv => {
  if (!nv) return;
  setValues({
    title: nv.title,
    short_description: nv.short_description,
    description: nv.description,
    remark: nv.remark,
    weight: nv.weight,
  });
}, { immediate: true });

const { mutate } = useApplicationMutation({ name: 'author.applications' });

const errorMessage: Ref<string|null> = ref(null);
const onSubmitForm = handleSubmit(async values => {
  errorMessage.value = null;
  const payload: Application = {
    id: props.id,
    name: application.value!.name,
    title: values.title,
    short_description: values.short_description,
    description: values.description,
    events: application.value!.events,
    news: application.value!.news,
    pages: application.value!.pages,
    remark: values.remark,
    weight: values.weight,
  };
  mutate(payload);
});
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>Wijzig Applicatie</ContainerSectionTitle>
    <ContainerSectionContent>
      <form class="w-full md:w-2/3 bg-zinc-50 rounded-lg p-3">
        <InputField
          name="title"
          :placeholder="t('applications.edit.form.title.placeholder')"
          class="pb-6"
          :required="true"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('applications.edit.form.title.label') }}&nbsp;:
            </span>
          </template>
        </InputField>
        <TextareaField
          name="short_description"
          :placeholder="t('applications.edit.form.short_description.placeholder')"
          class="pb-6"
          :rows="5"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('applications.edit.form.short_description.label') }}&nbsp;:
            </span>
          </template>
        </TextareaField>
        <TextareaField
          name="description"
          :placeholder="t('applications.edit.form.description.placeholder')"
          class="pb-6"
          :rows="10"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('applications.edit.form.description.label') }}&nbsp;:
            </span>
          </template>
        </TextareaField>
        <TextareaField
          name="remark"
          :placeholder="t('applications.edit.form.remark.placeholder')"
          class="pb-6"
          :rows="5"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('applications.edit.form.remark.label') }}&nbsp;:
            </span>
          </template>
        </TextareaField>
        <div class="flex flex-col items-end mt-6">
          <Button
            id="submit"
            class="bg-yellow-300 text-gray-600 border border-yellow-300 focus:bg-white focus:ring-2 focus:ring-yellow-300 hover:bg-white hover:border hover:border-yellow-300"
            @click="onSubmitForm"
          >
            {{ t('applications.edit.form.submit.label') }}
          </Button>
        </div>
      </form>
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
