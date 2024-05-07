<script setup lang="ts">
import type { TrainingDefinition } from '@root/composables/useTrainingDefinition';
import { computed, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useForm } from 'vee-validate';

import {
  Button,
  CheckBox,
  ErrorAlert,
  FormSection,
  FormSectionFields,
  InputField,
  SelectOption,
  TextareaField,
  TimePicker,
  isStringRequired,
} from '@kwai/ui';
import type { Option, TimeModel } from '@kwai/ui';
import { now, weekdays } from '@kwai/date';
import { useTeams } from '@root/composables/useTeam';
import { useTrainingDefinitionMutation } from '@root/composables/useTrainingDefinition';
import { useGoBack } from '@root/composables/useGoBack';

interface Props {
  definition?: TrainingDefinition
}
const props = defineProps<Props>();

const { t } = useI18n({ useScope: 'global' });

const { data: teams } = useTeams();
const teamOptions = computed((): Option[] => {
  const options = teams.value?.map(team => ({
    value: team.id,
    text: team.name,
  })) ?? [];
  options.unshift({ value: '', text: 'Geen' });
  return options;
});

const weekdayOptions = computed(():Option[] => {
  return weekdays().map((dayName, index) => ({ value: index, text: dayName }));
});
interface TrainingDefinitionForm {
  name: string,
  description: string,
  weekday: number,
  team: string | null,
  start_time: TimeModel | null,
  end_time: TimeModel | null,
  location: string,
  active: boolean,
  remark: string
}

const isTimeRequired = (value: TimeModel) => {
  if (value) return true;
  return t('training_definition.form.validations.required');
};

const isEndTimeValid = (value: TimeModel | null) => {
  if (value) {
    if (values.start_time) {
      const startTime = now()
        .set('hours', values.start_time.hours as number)
        .set('minutes', values.start_time.minutes as number)
      ;
      const endTime = now()
        .set('hours', value.hours as number)
        .set('minutes', value.minutes as number)
      ;
      if (endTime.isBefore(startTime)) {
        return t('training_definition.form.validations.end_time_before');
      }
    }
  }
  return true;
};

const { handleSubmit, resetForm, values } = useForm<TrainingDefinitionForm>({
  validationSchema: {
    name: isStringRequired(t('training_definition.form.validations.required')),
    description: isStringRequired(t('training_definition.form.validations.required')),
    start_time: isTimeRequired,
    end_time: [isTimeRequired, isEndTimeValid],
  },
  initialValues: {
    name: '',
    description: '',
    team: null,
    weekday: now().dayOfWeek(),
    start_time: null,
    end_time: null,
    location: '',
    active: false,
    remark: '',
  },
});

const goBack = useGoBack('coach.training_definitions');
const { mutate } = useTrainingDefinitionMutation({
  onSuccess: async() => await goBack(),
});

const errorMessage = ref<string>('');
const onSubmitForm = handleSubmit(async values => {
  let team = null;
  if (values.team !== '' && teams.value) {
    team = teams.value.find(team => team.id === values.team) ?? null;
  }
  errorMessage.value = '';
  const payload: TrainingDefinition = {
    location: values.location,
    weekday: values.weekday,
    start_time: now()
      .set('hours', values.start_time!.hours as number)
      .set('minutes', values.start_time!.minutes as number),
    end_time: now()
      .set('hours', values.end_time!.hours as number)
      .set('minutes', values.end_time!.minutes as number),
    timezone: 'Europe/Brussels',
    active: values.active,
    description: values.description,
    name: values.name,
    remark: values.remark,
    team,
    id: definition.value?.id,
  };
  mutate(payload, {
    onError: error => {
      errorMessage.value = error.message;
    },
  });
});

const definition = computed(() => props.definition);
watch(definition, nv => {
  if (!nv) return;
  const startTime = {
    hours: nv.start_time.get('hours'),
    minutes: nv.start_time.get('minutes'),
  };
  const endTime = {
    hours: nv.end_time.get('hours'),
    minutes: nv.end_time.get('minutes'),
  };
  resetForm({
    values: {
      name: nv.name,
      active: nv.active,
      description: nv.description,
      team: nv.team?.id || null,
      weekday: nv.weekday,
      start_time: startTime,
      end_time: endTime,
      location: nv.location,
    },
  });
});
</script>

<template>
  <form class="w-full bg-gray-200 rounded-lg p-3 grid gap-3">
    <FormSection :title="t('training_definition.form.sections.definition.title')">
      <template #description>
        {{ t('training_definition.form.sections.definition.description') }}
      </template>
      <FormSectionFields class="bg-white p-3">
        <InputField
          name="name"
          :placeholder="t('training_definition.form.sections.definition.fields.name.placeholder')"
          :required="true"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('training_definition.form.sections.definition.fields.name.label') }}&nbsp;:
            </span>
          </template>
        </InputField>
        <TextareaField
          name="description"
          :placeholder="t('training_definition.form.sections.definition.fields.description.placeholder')"
          :rows="5"
          :required="true"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('training_definition.form.sections.definition.fields.description.label') }}&nbsp;:
            </span>
          </template>
        </TextareaField>
      </FormSectionFields>
    </FormSection>
    <FormSection :title="t('training_definition.form.sections.team.title')">
      <template #description>
        {{ t('training_definition.form.sections.team.description') }}
      </template>
      <FormSectionFields class="bg-white p-3">
        <SelectOption
          name="team"
          :options="teamOptions"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('training_definition.form.sections.team.fields.team.label') }}&nbsp;:
            </span>
          </template>
        </SelectOption>
      </FormSectionFields>
    </FormSection>
    <FormSection :title="t('training_definition.form.sections.period.title')">
      <template #description>
        {{ t('training_definition.form.sections.period.description') }}
      </template>
      <FormSectionFields class="bg-white p-3">
        <SelectOption
          name="weekday"
          :options="weekdayOptions"
          :required="true"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('training_definition.form.sections.period.fields.weekday.label') }}&nbsp;:
            </span>
          </template>
        </SelectOption>
        <TimePicker
          name="start_time"
          :required="true"
          :placeholder="t('training_definition.form.sections.period.fields.start_time.placeholder')"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('training_definition.form.sections.period.fields.start_time.label') }}&nbsp;:
            </span>
          </template>
        </TimePicker>
        <TimePicker
          name="end_time"
          :required="true"
          :placeholder="t('training_definition.form.sections.period.fields.end_time.placeholder')"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('training_definition.form.sections.period.fields.end_time.label') }}&nbsp;:
            </span>
          </template>
        </TimePicker>
      </FormSectionFields>
    </FormSection>
    <FormSection :title="t('training.form.sections.remark.title')">
      <template #description>
        {{ t('training_definition.form.sections.remark.description') }}
      </template>
      <FormSectionFields class="bg-white">
        <TextareaField
          name="remark"
          :placeholder="t('training_definition.form.sections.remark.fields.remark.placeholder')"
          :rows="5"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('training_definition.form.sections.remark.fields.remark.label') }}&nbsp;:
            </span>
          </template>
        </TextareaField>
      </FormSectionFields>
    </FormSection>
    <FormSection>
      <FormSectionFields class="bg-white">
        <CheckBox
          name="active"
          :label="t('training_definition.form.sections.submit.fields.active.label')"
        >
          <template #help>
            {{ t('training_definition.form.sections.submit.fields.active.help') }}
          </template>
        </CheckBox>
        <div class="flex flex-col items-end mt-6">
          <Button
            id="submit"
            class="font-medium text-sm text-white outline-none focus:outline-none rounded border border-orange-500 disabled:bg-orange-300 bg-orange-500 hover:bg-white hover:disabled:text-white hover:text-black focus:ring-2 focus:ring-orange-500"
            @click="onSubmitForm"
          >
            {{ t('training_definition.form.sections.submit.fields.button.label') }}
          </Button>
        </div>
        <ErrorAlert v-if="errorMessage">
          {{ t('training_definition.form.error') }}
        </ErrorAlert>
      </FormSectionFields>
    </FormSection>
  </form>
</template>

<style scoped>

</style>
