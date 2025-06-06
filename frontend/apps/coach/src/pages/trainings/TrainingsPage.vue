<script setup lang="ts">
import { useTrainings } from '@root/composables/useTraining';
import {
  ContainerSection,
  ContainerSectionTitle,
  ContainerSectionContent,
  NewIcon,
  KwaiWarningAlert,
  CancelIcon,
  CheckIcon,
  EditIcon,
  KwaiButton,
  KwaiMonthPicker,
  KwaiTag,
  KwaiToolbar,
} from '@kwai/ui';
import {
  createDate, createFromDate, now,
} from '@kwai/date';
import {
  computed, ref, watch,
} from 'vue';
import {
  useRoute, useRouter,
} from 'vue-router';
import { useI18n } from 'vue-i18n';
import NowIcon from '@root/components/icons/NowIcon.vue';
import { useForm } from 'vee-validate';

const { t } = useI18n({ useScope: 'global' });

const route = useRoute();

const toDay = now();
const currentMonth = ref(toDay.month());
const currentYear = ref(toDay.year());

const year = computed(() => {
  if (route.query.year) {
    return Number.parseInt(route.query.year as string ?? currentYear.value);
  }
  return currentYear.value;
});
const month = computed(() => {
  if (route.query.month) {
    return Number.parseInt(route.query.month as string) - 1;
  }
  return currentMonth.value;
});

const start = computed(() => createDate(year.value, month.value).startOf('month'));
const end = computed(() => createDate(year.value, month.value).endOf('month'));
const { data: trainings } = useTrainings({
  start, end,
});

const title = computed(() => start.value.format('MMMM'));

const { defineField } = useForm();
const [selectedMonth] = defineField('month');
selectedMonth.value = createDate(year.value, month.value).toDate();

const router = useRouter();
watch(selectedMonth, (nv) => {
  if (nv) {
    const date = createFromDate(nv);
    router.replace({
      query: {
        ...route.query,
        month: date.month() + 1,
        year: date.year(),
      },
    });
  }
});

const setToCurrent = () => {
  selectedMonth.value = now().toDate();
};
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>
      {{ t('trainings.title') }} <span class="capitalize">{{ title }}</span> {{ start.format("YYYY") }}
    </ContainerSectionTitle>
    <ContainerSectionContent>
      <KwaiToolbar>
        <template #start>
          <div class="flex flex-col">
            <h5 class="mr-3 font-semibold">
              {{ t('trainings.banner.title') }}
            </h5>
            <p class="text-gray-500">
              {{ t('trainings.banner.description') }}
            </p>
          </div>
        </template>
        <template #center>
          <form
            class="relative flex flex-row space-x-4 items-center"
            novalidate
          >
            <KwaiMonthPicker
              name="month"
            />
            <KwaiButton :method="setToCurrent">
              <template #icon>
                <NowIcon class="w-4 fill-current" />
              </template>
            </KwaiButton>
          </form>
        </template>
        <template #end>
          <KwaiButton :to="{ name: 'coach.trainings.create' }">
            <template #icon>
              <NewIcon class="w-4 mr-2 fill-current" />
            </template>
            {{ t('trainings.banner.button') }}
          </KwaiButton>
        </template>
      </KwaiToolbar>
      <KwaiWarningAlert v-if="trainings && trainings.meta.count === 0">
        Er zijn geen trainingen voor deze maand.
      </KwaiWarningAlert>
      <div
        v-if="trainings && trainings.meta.count > 0"
        class="relative w-full overflow-x-auto"
      >
        <table class="w-full text-sm text-left rtl:text-right">
          <thead class="text-xs text-gray-700 uppercase bg-gray-50">
            <tr>
              <th
                scope="col"
                class="px-6 py-3"
              >
                {{ t('trainings.table.columns.date') }}
              </th>
              <th
                scope="col"
                class="px-6 py-3"
              >
                {{ t('trainings.table.columns.hours') }}
              </th>
              <th
                scope="col"
                class="px-6 py-3"
              >
                {{ t('trainings.table.columns.title') }}
              </th>
              <th
                scope="col"
                class="px-6 py-3"
              >
                {{ t('trainings.table.columns.active') }}
              </th>
              <th
                scope="col"
                class="px-6 py-3"
              />
            </tr>
          </thead>
          <tbody>
            <template
              v-for="training in trainings.items"
              :key="training.id"
            >
              <tr class="border-b">
                <td class="px-6 py-4">
                  {{ training.start_date.format("DD-MM-YYYY") }}
                </td>
                <td class="px-6 py-4">
                  {{ training.start_date.format("HH:mm") }} - {{ training.end_date.format("HH:mm") }}
                </td>
                <td class="px-6 py-4">
                  {{ training.texts[0].title }}
                  <KwaiTag
                    v-if="training.cancelled"
                    severity="danger"
                  >
                    {{ t('trainings.table.cancelled') }}
                  </KwaiTag>
                </td>
                <td class="px-6 py-4">
                  <CheckIcon
                    v-if="training.enabled"
                    class="w-4 fill-green-600 font-bold"
                  />
                  <CancelIcon
                    v-else
                    class="w-f4 fill-red-500 font-bold"
                  />
                </td>
                <td class="px-6 py-4">
                  <KwaiButton :to="{ name: 'coach.trainings.edit', params: { id: training.id } }">
                    <EditIcon class="w-4 fill-current" />
                  </KwaiButton>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>
</style>
