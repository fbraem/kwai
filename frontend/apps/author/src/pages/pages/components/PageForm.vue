<script setup lang="ts">
import {
  KwaiButton,
  KwaiCheckboxField,
  ErrorAlert,
  FormSection,
  FormSectionFields,
  InputField,
  KwaiSlider,
  SelectOption,
  TextareaField,
} from '@kwai/ui';
import type { Option } from '@kwai/ui';
import { useI18n } from 'vue-i18n';
import { useForm } from 'vee-validate';
import type { ApplicationForAuthor } from '@root/composables/useApplication';
import { computed, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import type { PageForAuthor } from '@root/composables/usePage';
import { usePageMutation } from '@root/composables/usePage';
import type { Application } from '@kwai/types';

interface Props {
  page?: PageForAuthor | null,
  applications?: ApplicationForAuthor[]
}
const props = defineProps<Props>();
const page = computed(() => props.page);
const applications = computed(() => props.applications);

const { t } = useI18n({ useScope: 'global' });

const applicationOptions = computed(():Option[] => {
  return applications.value?.map(
    application => ({ value: application, text: application.title })
  ) ?? [];
});

function isRequired(value: string): string|boolean {
  if (value && value.trim()) {
    return true;
  }
  return t('pages.form.validations.required');
}
interface PageForm {
  title: string,
  summary: string,
  content: string,
  active: boolean,
  priority: number,
  remark: string,
  application: Application | null,
}
const { handleSubmit, setValues } = useForm<PageForm>({
  validationSchema: {
    title: isRequired,
    summary: isRequired,
    application: (value: ApplicationForAuthor) => {
      if (value) return true;
      return t('pages.form.validations.required');
    },
    content: isRequired,
  },
  initialValues: {
    title: '',
    summary: '',
    content: '',
    active: false,
    priority: 0,
    remark: '',
    application: null,
  },
});

watch(page, nv => {
  console.log('does not work?');
  if (!nv) return;
  // The value of the applications select comes from applications.
  // So we need that value from the list, not the one from the page item.
  const application = applications.value?.find(application => application.id === nv.application.id);

  setValues({
    title: nv.texts[0].title,
    summary: nv.texts[0].originalSummary,
    content: nv.texts[0].originalContent ?? '',
    application,
    priority: nv.priority,
    remark: nv.remark,
    active: nv.enabled,
  });
}, { immediate: true });

const router = useRouter();
const goBack = async() => {
  if (router.options.history.state.back) {
    router.go(-1);
  }
  await router.replace({ name: 'author.pages' });
};
const { mutate } = usePageMutation({
  onSuccess: async() => await goBack(),
});

const errorMessage = ref<string>('');
const onSubmitForm = handleSubmit(async values => {
  errorMessage.value = '';
  const payload: PageForAuthor = {
    application: values.application!,
    id: page.value?.id,
    enabled: values.active ?? false,
    remark: values.remark ?? '',
    priority: values.priority,
    texts: [
      {
        format: 'md',
        locale: 'nl',
        title: values.title,
        originalSummary: values.summary,
        summary: page?.value?.texts[0]?.summary ?? '',
        content: page?.value?.texts[0]?.content ?? '',
        originalContent: values.content,
      },
    ],
  };
  mutate(payload, {
    onError: error => {
      errorMessage.value = error.message;
    },
  });
});
</script>

<template>
  <form class="w-full bg-gray-200 rounded-lg p-3 grid gap-3">
    <FormSection :title="t('pages.form.sections.page.title')">
      <template #description>
        {{ t('pages.form.sections.page.description') }}
      </template>
      <FormSectionFields class="bg-white p-3">
        <InputField
          name="title"
          :placeholder="t('pages.form.sections.page.fields.title.placeholder')"
          class="pb-6"
          :required="true"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('pages.form.sections.page.fields.title.label') }}&nbsp;:
            </span>
          </template>
        </InputField>
        <TextareaField
          name="summary"
          :placeholder="t('pages.form.sections.page.fields.summary.placeholder')"
          class="pb-6"
          :rows="5"
          :required="true"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('pages.form.sections.page.fields.summary.label') }}&nbsp;:
            </span>
          </template>
        </TextareaField>
        <TextareaField
          name="content"
          :placeholder="t('pages.form.sections.page.fields.content.placeholder')"
          :rows="10"
          :required="true"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('pages.form.sections.page.fields.content.label') }}&nbsp;:
            </span>
          </template>
        </TextareaField>
      </FormSectionFields>
    </FormSection>
    <FormSection :title="t('pages.form.sections.application.title')">
      <template #description>
        {{ t('pages.form.sections.application.description') }}
      </template>
      <FormSectionFields class="bg-white">
        <SelectOption
          name="application"
          :options="applicationOptions"
          :required="true"
        >
          <template #label>
            {{ t('pages.form.sections.application.fields.application.label') }} :
          </template>
        </SelectOption>
      </FormSectionFields>
    </FormSection>
    <FormSection :title="t('pages.form.sections.promotion.title')">
      <template #description>
        {{ t('pages.form.sections.promotion.description') }}
      </template>
      <FormSectionFields class="bg-white">
        <KwaiSlider
          name="priority"
          class="pb-6"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('pages.form.sections.promotion.fields.priority.label') }}&nbsp;:
            </span>
          </template>
        </KwaiSlider>
      </FormSectionFields>
    </FormSection>
    <FormSection :title="t('pages.form.sections.remark.title')">
      <template #description>
        {{ t('pages.form.sections.remark.description') }}
      </template>
      <FormSectionFields class="bg-white">
        <TextareaField
          name="remark"
          :placeholder="t('pages.form.sections.remark.fields.remark.placeholder')"
          :rows="5"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('pages.form.sections.remark.fields.remark.label') }}&nbsp;:
            </span>
          </template>
        </TextareaField>
      </FormSectionFields>
    </FormSection>
    <FormSection>
      <FormSectionFields class="bg-white">
        <KwaiCheckboxField
          name="active"
        >
          <template #label>
            {{ t('pages.form.sections.submit.fields.active.label') }}
          </template>
          <template #help>
            {{ t('pages.form.sections.submit.fields.active.help') }}
          </template>
        </KwaiCheckboxField>
        <div class="flex flex-col items-end mt-6">
          <KwaiButton
            id="submit"
            :method="onSubmitForm"
          >
            {{ t('pages.form.sections.submit.fields.button.label') }}
          </KwaiButton>
        </div>
        <ErrorAlert v-if="errorMessage">
          {{ t('pages.form.error') }}
        </ErrorAlert>
      </FormSectionFields>
    </FormSection>
  </form>
</template>

<style scoped>

</style>
