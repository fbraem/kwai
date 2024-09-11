<script setup lang="ts">
import { useTrainingDefinition } from '@root/composables/useTrainingDefinition';
import {
  CheckIcon,
  ContainerSection,
  ContainerSectionBanner,
  ContainerSectionContent,
  ContainerSectionTitle,
  DateRangePicker,
  DeleteIcon,
  InfoAlert,
  KwaiButton,
  LinkTag,
  NewIcon,
} from '@kwai/ui';
import { useI18n } from 'vue-i18n';
import TrainingDefinitionCard from '@root/pages/training_definitions/components/TrainingDefinitionCard.vue';
import { ref, toRef } from 'vue';
import { useForm } from 'vee-validate';
import { createFromDate, now } from '@kwai/date';
import type { Training } from '@root/composables/useTraining';
import { generateTrainings } from '@root/composables/useTrainingGenerator';
import { useTrainingMutation } from '@root/composables/useTraining';

interface Props {
  id: string
}
const props = defineProps<Props>();
const id = toRef(props.id);

const { data: trainingDefinition } = useTrainingDefinition(id);

const { t } = useI18n({ useScope: 'global' });

interface GenerateForm {
  period: Date[]
}
const { handleSubmit } = useForm<GenerateForm>({
  initialValues: {
    period: [
      now().startOf('month').toDate(),
      now().endOf('month').toDate(),
    ],
  },
});

const trainings = ref<Training[]>([]);

const onSubmitForm = handleSubmit(values => {
  trainings.value = generateTrainings(
    trainingDefinition.value!,
    createFromDate(values.period[0]),
    createFromDate(values.period[1])
  );
});

const remove = (index: number) => {
  trainings.value.splice(index, 1);
};

const { mutate } = useTrainingMutation({
  onSuccess: (resource: Training, context) => {
    trainings.value[context!.index] = resource;
  },
});
const saveTrainings = () => {
  trainings.value.forEach((training, index) => {
    if (!training.id) {
      mutate({ training, context: { index } });
    }
  });
};

</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>
      {{ t('generate_trainings.title') }}
    </ContainerSectionTitle>
    <ContainerSectionContent>
      <TrainingDefinitionCard
        v-if="trainingDefinition"
        :training-definition="trainingDefinition"
      />
      <ContainerSectionBanner>
        <template #left>
          <h5 class="mr-3 font-semibold">
            {{ t('generate_trainings.banner.title') }}
          </h5>
          <p class="text-gray-500 text-sm">
            {{ t('generate_trainings.banner.description') }}
          </p>
        </template>
        <template #right>
          <div class="flex sm:flex-col gap-4">
            <DateRangePicker
              name="period"
              :time="false"
            />
            <KwaiButton :method="onSubmitForm">
              <NewIcon class="w-4 mr-2 fill-current" />
              {{ t('generate_trainings.banner.button') }}
            </KwaiButton>
          </div>
        </template>
      </ContainerSectionBanner>
      <table
        v-if="trainings.length > 0"
        class="w-full text-sm text-left rtl:text-right"
      >
        <thead class="text-xs text-gray-700 uppercase bg-gray-50">
          <tr>
            <th
              scope="col"
              class="px-6 py-3"
            >
              {{ t('generate_trainings.table.columns.date') }}
            </th>
            <th
              scope="col"
              class="px-6 py-3"
            >
              {{ t('generate_trainings.table.columns.period') }}
            </th>
            <th
              scope="col"
              class="px-6 py-3"
            >
              {{ t('generate_trainings.table.columns.title') }}
            </th>
            <th
              scope="col"
              class="px-6 py-3"
            />
          </tr>
        </thead>
        <tr
          v-for="(training, index) in trainings"
          :key="`training-${index}`"
        >
          <th class="px-6 py-3">
            {{ training.start_date.format('ddd') }} {{ training.start_date.format("DD-MM-YYYY") }}
          </th>
          <td class="px-6 py-3">
            {{ training.start_date.format("HH:mm") }} -
            {{ training.end_date.format("HH:mm") }}
          </td>
          <td class="px-6 py-3">
            {{ training.texts[0].title }}
          </td>
          <td>
            <CheckIcon
              v-if="training.id"
              class="w-4 fill-green-600 font-bold"
            />
            <LinkTag
              v-else
              :method="() => remove(index)"
              class="border-none text-base inline-flex justify-center items-center align-middle no-underline rounded-full cursor-pointer focus:outline-none hover:no-underline hover:bg-red-200 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed p-2"
            >
              <DeleteIcon class="w-4 fill-red-500" />
            </LinkTag>
          </td>
        </tr>
      </table>
      <div
        v-if="trainings.length > 0"
        class="w-full flex flex-col"
      >
        <KwaiButton :method="saveTrainings">
          <NewIcon class="w-4 mr-2 fill-current" />
          {{ t('generate_trainings.save') }}
        </KwaiButton>
      </div>
      <div v-else>
        <InfoAlert>
          {{ t('generate_trainings.no_trainings') }}
        </InfoAlert>
      </div>
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
