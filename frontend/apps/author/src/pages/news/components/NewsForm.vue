<script setup lang="ts">
import {
  KwaiButton,
  KwaiCheckbox,
  KwaiDatePicker,
  KwaiDateRangePicker,
  ErrorAlert,
  FormSection,
  FormSectionFields,
  InputField,
  KwaiSlider,
  SelectOption,
  TextareaField,
} from '@kwai/ui';
import type { Option } from '@kwai/ui';
import type { NewsItemForAuthor } from '@root/composables/useNewsItem';
import { useI18n } from 'vue-i18n';
import { useForm } from 'vee-validate';
import type { ApplicationForAuthor } from '@root/composables/useApplication';
import { computed, ref, watch } from 'vue';
import { now, createFromDate } from '@kwai/date';
import { useRouter } from 'vue-router';
import { useNewsItemMutation } from '@root/composables/useNewsItem';
import type { Application } from '@kwai/types';

interface Props {
  newsItem?: NewsItemForAuthor | null,
  applications?: ApplicationForAuthor[]
}
const props = defineProps<Props>();
const newsItem = computed(() => props.newsItem);
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
  return t('news.form.validations.required');
}
interface NewsItemForm {
    title: string,
    summary: string,
    content: string,
    priority: number,
    active: boolean,
    remark: string,
    promotion_end_timestamp: Date | null,
    application: Application | null,
    publication_period: (Date | null)[],
}
const { handleSubmit, setValues } = useForm<NewsItemForm>({
  validationSchema: {
    title: isRequired,
    summary: isRequired,
    application: (value: ApplicationForAuthor) => {
      if (value) return true;
      return t('news.form.validations.required');
    },
    publication_period: (values: (Date | null)[]) => {
      if (values) {
        return values.length >= 0 && values[0];
      }
      return t('news.form.validations.required');
    },
  },
  initialValues: {
    title: '',
    summary: '',
    content: '',
    priority: 0,
    active: false,
    remark: '',
    promotion_end_timestamp: null,
    application: null,
    publication_period: [now().toDate(), null],
  },
});

watch(newsItem, nv => {
  if (!nv) return;
  // The value of the applications select comes from applications.
  // So we need that value from the list, not the one from the news item.
  const application = applications.value?.find(application => application.id === nv.application.id);

  setValues({
    title: nv.texts[0].title,
    summary: nv.texts[0].originalSummary,
    content: nv.texts[0].originalContent ?? '',
    priority: nv.priority,
    promotion_end_timestamp: nv.promotionEndDate?.toDate(),
    application,
    publication_period: [nv.publishDate.toDate(), nv.endDate?.toDate() ?? null],
    remark: nv.remark,
    active: nv.enabled,
  });
}, { immediate: true });

const router = useRouter();
const goBack = async() => {
  if (router.options.history.state.back) {
    router.go(-1);
  }
  await router.replace({ name: 'author.news' });
};
const { mutate } = useNewsItemMutation({
  onSuccess: async() => await goBack(),
});

const errorMessage = ref<string>('');
const onSubmitForm = handleSubmit(async values => {
  errorMessage.value = '';
  const payload: NewsItemForAuthor = {
    application: values.application!,
    id: newsItem.value?.id,
    enabled: values.active ?? false,
    priority: values.priority,
    publishDate: createFromDate(values.publication_period[0]!),
    endDate: values.publication_period[1] ? createFromDate(values.publication_period[1]) : null,
    promotionEndDate: values.promotion_end_timestamp ? createFromDate(values.promotion_end_timestamp) : null,
    remark: values.remark ?? '',
    texts: [
      {
        format: 'md',
        locale: 'nl',
        title: values.title,
        originalSummary: values.summary,
        summary: newsItem?.value?.texts[0]?.summary ?? '',
        content: newsItem?.value?.texts[0]?.content ?? '',
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
    <FormSection :title="t('news.form.sections.news_item.title')">
      <template #description>
        {{ t('news.form.sections.news_item.description') }}
      </template>
      <FormSectionFields class="bg-white p-3">
        <InputField
          name="title"
          :placeholder="t('news.form.sections.news_item.fields.title.placeholder')"
          class="pb-6"
          :required="true"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('news.form.sections.news_item.fields.title.label') }}&nbsp;:
            </span>
          </template>
        </InputField>
        <TextareaField
          name="summary"
          :placeholder="t('news.form.sections.news_item.fields.summary.placeholder')"
          class="pb-6"
          :rows="5"
          :required="true"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('news.form.sections.news_item.fields.summary.label') }}&nbsp;:
            </span>
          </template>
        </TextareaField>
        <TextareaField
          name="content"
          :placeholder="t('news.form.sections.news_item.fields.content.placeholder')"
          :rows="10"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('news.form.sections.news_item.fields.content.label') }}&nbsp;:
            </span>
          </template>
        </TextareaField>
      </FormSectionFields>
    </FormSection>
    <FormSection :title="t('news.form.sections.application.title')">
      <template #description>
        {{ t('news.form.sections.application.description') }}
      </template>
      <FormSectionFields class="bg-white">
        <SelectOption
          name="application"
          :options="applicationOptions"
          :required="true"
        >
          <template #label>
            {{ t('news.form.sections.application.fields.application.label') }} :
          </template>
        </SelectOption>
      </FormSectionFields>
    </FormSection>
    <FormSection :title="t('news.form.sections.publication.title')">
      <template #description>
        {{ t('news.form.sections.publication.description') }}
      </template>
      <FormSectionFields class="bg-white">
        <KwaiDateRangePicker
          name="publication_period"
          :placeholder="t('news.form.sections.publication.fields.start_date.placeholder')"
          :time="true"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('news.form.sections.publication.fields.start_date.label') }}&nbsp;:
            </span>
          </template>
        </KwaiDateRangePicker>
      </FormSectionFields>
    </FormSection>
    <FormSection :title="t('news.form.sections.promotion.title')">
      <template #description>
        {{ t('news.form.sections.promotion.description') }}
      </template>
      <FormSectionFields class="bg-white">
        <KwaiSlider
          name="priority"
          class="pb-6"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('news.form.sections.promotion.fields.priority.label') }}&nbsp;:
            </span>
          </template>
        </KwaiSlider>
        <KwaiDatePicker
          name="promotion_end_timestamp"
          :placeholder="t('news.form.sections.promotion.fields.end_timestamp.placeholder')"
          :time="true"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('news.form.sections.promotion.fields.end_timestamp.label') }}&nbsp;:
            </span>
          </template>
        </KwaiDatePicker>
      </FormSectionFields>
    </FormSection>
    <FormSection :title="t('news.form.sections.remark.title')">
      <template #description>
        {{ t('news.form.sections.remark.description') }}
      </template>
      <FormSectionFields class="bg-white">
        <TextareaField
          name="remark"
          :placeholder="t('news.form.sections.remark.fields.remark.placeholder')"
          :rows="5"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('news.form.sections.remark.fields.remark.label') }}&nbsp;:
            </span>
          </template>
        </TextareaField>
      </FormSectionFields>
    </FormSection>
    <FormSection>
      <FormSectionFields class="bg-white">
        <KwaiCheckbox name="active">
          <template #label>
            {{ t('news.form.sections.submit.fields.active.label') }}
          </template>
          <template #help>
            {{ t('news.form.sections.submit.fields.active.help') }}
          </template>
        </KwaiCheckbox>
        <div class="flex flex-col items-end mt-6">
          <KwaiButton
            id="submit"
            :method="onSubmitForm"
          >
            {{ t('news.form.sections.submit.fields.button.label') }}
          </KwaiButton>
        </div>
        <ErrorAlert v-if="errorMessage">
          {{ t('news.form.error') }}
        </ErrorAlert>
      </FormSectionFields>
    </FormSection>
  </form>
</template>

<style scoped>

</style>
