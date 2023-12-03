<script setup lang="ts">
import {
  Button,
  CheckBox,
  DatePicker,
  ErrorAlert,
  FormSection,
  FormSectionFields,
  InputField,
  SelectOption,
  TextareaField,
} from '@kwai/ui';
import type { Option } from '@kwai/ui';
import { useI18n } from 'vue-i18n';
import type { Training } from '@root/composables/useTraining';
import type { TrainingDefinition } from '@root/composables/useTrainingDefinition';
import { computed, ref, watch } from 'vue';
import { useField, useForm } from 'vee-validate';
import { createFromDate, getLocaleFormat, weekdays } from '@kwai/date';
import PrimaryButton from '@root/components/PrimaryButton.vue';
import { useRouter } from 'vue-router';
import { useTrainingMutation } from '@root/composables/useTraining';

interface Props {
  training?: Training | null,
  definitions?: TrainingDefinition[]
}
const props = defineProps<Props>();
const training = computed(() => props.training);
const definitions = computed(() => props.definitions);

const { t } = useI18n({ useScope: 'global' });

const definitionOptions = computed((): Option[] => {
  const weekdayList = weekdays();
  const options = definitions.value?.map(
    definition => ({ value: definition.id, text: definition.name + ' - ' + weekdayList[definition.weekday] })
  ) ?? [];
  options.unshift({ value: '', text: 'Geen' });
  return options;
});

function isRequired(value: string): string|boolean {
  if (value && value.trim()) {
    return true;
  }
  return t('training.form.validations.required');
}

const dateFormat = ref('ddd ' + getLocaleFormat('L') + ' HH:mm');

interface TrainingForm {
  active: boolean,
  cancelled: boolean,
  content: string,
  definition: string | null,
  end_date: Date | null,
  location: string,
  remark: string,
  start_date: Date | null,
  summary: string,
  title: string
}

const { setFieldValue, handleSubmit, resetForm } = useForm<TrainingForm>({
  validationSchema: {
    title: isRequired,
    summary: isRequired,
  },
  initialValues: {
    active: false,
    cancelled: false,
    content: '',
    definition: null,
    end_date: null,
    location: '',
    remark: '',
    start_date: null,
    summary: '',
    title: '',
  },
});

watch(training, nv => {
  if (!nv) return;
  // The value of the definitions select comes from training definitions.
  // So we need that value from the list, not the one from the training.
  resetForm({
    values: {
      active: nv.enabled,
      cancelled: nv.cancelled,
      content: nv.texts[0].originalContent ?? '',
      definition: nv.definition?.id ?? '',
      end_date: nv.end_date.toDate(),
      location: nv.location ?? '',
      remark: nv.remark,
      start_date: nv.start_date.toDate(),
      summary: nv.texts[0].originalSummary,
      title: nv.texts[0].title,
    },
  });
}, { immediate: true });

const router = useRouter();
const goBack = async() => {
  if (router.options.history.state.back) {
    router.go(-1);
  }
  await router.replace({ name: 'coach.trainings' });
};

const { mutate } = useTrainingMutation({
  onSuccess: async() => await goBack(),
});

const errorMessage = ref<string>('');
const onSubmitForm = handleSubmit(async values => {
  let definition = null;
  if (values.definition !== '' && definitions.value) {
    definition = definitions.value.find(definition => definition.id === values.definition) ?? null;
  }
  errorMessage.value = '';
  const payload: Training = {
    cancelled: values.cancelled,
    texts: [
      {
        format: 'md',
        locale: 'nl',
        title: values.title,
        originalSummary: values.summary,
        summary: training?.value?.texts[0]?.summary ?? '',
        content: training?.value?.texts[0]?.content ?? '',
        originalContent: values.content,
      },
    ],
    definition,
    enabled: values.active,
    end_date: createFromDate(values.end_date!),
    id: training.value?.id,
    location: values.location,
    remark: values.remark,
    start_date: createFromDate(values.start_date!),
    teams: training.value?.teams ?? [],
  };
  mutate(payload, {
    onError: error => {
      errorMessage.value = error.message;
    },
  });
});

const enableApplyDefinition = computed(() => {
  return String(definitionField.value.value) !== '';
});

const definitionField = useField<Option>('definition');
const startDateField = useField<Date|null>('start_date');
const endDateField = useField<Date|null>('end_date');
const applyDefinition = () => {
  const fieldValue = String(definitionField.value.value);
  if (fieldValue !== '') {
    const definition = definitions.value?.find(definition => definition.id === fieldValue) ?? null;
    if (definition) {
      setFieldValue('summary', definition.description);
      setFieldValue('title', definition.name);
      setFieldValue('location', definition.location);

      let date = createFromDate(startDateField.value.value ?? new Date());
      let diffDays = definition.weekday - date.dayOfWeek();
      let newDate = date
        .add(diffDays, 'day')
        .copy(definition.start_time, ['hour', 'minute'])
      ;
      setFieldValue('start_date', newDate.toDate());

      date = createFromDate(endDateField.value.value ?? new Date());
      diffDays = definition.weekday - date.dayOfWeek();
      newDate = date
        .add(diffDays, 'day')
        .copy(definition.end_time, ['hour', 'minute'])
      ;
      setFieldValue('end_date', newDate.toDate());
    }
  }
};
</script>

<template>
  <form class="w-full bg-gray-200 rounded-lg p-3 grid gap-3">
    <FormSection :title="t('training.form.sections.definition.title')">
      <template #description>
        {{ t('training.form.sections.definition.description') }}
      </template>
      <FormSectionFields class="bg-white">
        <div class="flex flex-row space-x-2">
          <div class="flex-grow">
            <SelectOption
              name="definition"
              :options="definitionOptions"
              :required="true"
            >
              <template #label>
                {{ t('training.form.sections.definition.fields.definition.label') }} :
              </template>
            </SelectOption>
          </div>
          <div class="self-end">
            <PrimaryButton
              :method="applyDefinition"
              :disabled="!enableApplyDefinition"
            >
              {{ t('training.form.sections.definition.fields.definition.apply') }}
            </PrimaryButton>
          </div>
        </div>
      </FormSectionFields>
    </FormSection>
    <FormSection :title="t('training.form.sections.training.title')">
      <template #description>
        {{ t('training.form.sections.training.description') }}
      </template>
      <FormSectionFields class="bg-white p-3">
        <InputField
          name="title"
          :placeholder="t('training.form.sections.training.fields.title.placeholder')"
          :required="true"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('training.form.sections.training.fields.title.label') }}&nbsp;:
            </span>
          </template>
        </InputField>
        <TextareaField
          name="summary"
          :placeholder="t('training.form.sections.training.fields.summary.placeholder')"
          :rows="5"
          :required="true"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('training.form.sections.training.fields.summary.label') }}&nbsp;:
            </span>
          </template>
        </TextareaField>
        <TextareaField
          name="content"
          :placeholder="t('training.form.sections.training.fields.content.placeholder')"
          :rows="10"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('training.form.sections.training.fields.content.label') }}&nbsp;:
            </span>
          </template>
        </TextareaField>
      </FormSectionFields>
    </FormSection>
    <FormSection :title="t('training.form.sections.date.title')">
      <template #description>
        {{ t('training.form.sections.date.description') }}
      </template>
      <FormSectionFields class="bg-white">
        <DatePicker
          name="start_date"
          :time="true"
          :placeholder="t('training.form.sections.date.fields.start_date.placeholder')"
          :required="true"
          :format="dateFormat"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('training.form.sections.date.fields.start_date.label') }}&nbsp;:
            </span>
          </template>
        </DatePicker>
        <DatePicker
          name="end_date"
          :time="true"
          :placeholder="t('training.form.sections.date.fields.end_date.placeholder')"
          :required="true"
          :format="dateFormat"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('training.form.sections.date.fields.end_date.label') }}&nbsp;:
            </span>
          </template>
        </DatePicker>
        <CheckBox
          name="cancelled"
          :label="t('training.form.sections.date.fields.cancelled.label')"
        >
          <template #help>
            {{ t('training.form.sections.date.fields.cancelled.help') }}
          </template>
        </CheckBox>
      </FormSectionFields>
    </FormSection>
    <FormSection :title="t('training.form.sections.location.title')">
      <template #description>
        {{ t('training.form.sections.location.description') }}
      </template>
      <FormSectionFields class="bg-white">
        <InputField
          name="location"
          :placeholder="t('training.form.sections.location.fields.location.placeholder')"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('training.form.sections.location.fields.location.label') }}&nbsp;:
            </span>
          </template>
        </InputField>
      </FormSectionFields>
    </FormSection>
    <FormSection :title="t('training.form.sections.remark.title')">
      <template #description>
        {{ t('training.form.sections.remark.description') }}
      </template>
      <FormSectionFields class="bg-white">
        <TextareaField
          name="remark"
          :placeholder="t('training.form.sections.remark.fields.remark.placeholder')"
          :rows="5"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('training.form.sections.remark.fields.remark.label') }}&nbsp;:
            </span>
          </template>
        </TextareaField>
      </FormSectionFields>
    </FormSection>
    <FormSection>
      <FormSectionFields class="bg-white">
        <CheckBox
          name="active"
          :label="t('training.form.sections.submit.fields.active.label')"
        >
          <template #help>
            {{ t('training.form.sections.submit.fields.active.help') }}
          </template>
        </CheckBox>
        <div class="flex flex-col items-end mt-6">
          <Button
            id="submit"
            class="bg-yellow-300 text-gray-600 border border-yellow-300 focus:bg-white focus:ring-2 focus:ring-yellow-300 hover:bg-white hover:border hover:border-yellow-300"
            @click="onSubmitForm"
          >
            {{ t('training.form.sections.submit.fields.button.label') }}
          </Button>
        </div>
        <ErrorAlert v-if="errorMessage">
          {{ t('training.form.error') }}
        </ErrorAlert>
      </FormSectionFields>
    </FormSection>
  </form>
</template>

<style scoped>

</style>
