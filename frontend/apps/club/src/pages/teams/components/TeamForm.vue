<script setup lang="ts">
import type { Team } from '@root/types/team';
import {
  KwaiErrorAlert,
  FormSection,
  FormSectionFields,
  KwaiCheckbox,
  KwaiButton,
  KwaiInputField,
  KwaiTextarea,
} from '@kwai/ui';
import { useI18n } from 'vue-i18n';
import { computed, ref, watch } from 'vue';
import { useForm } from 'vee-validate';
import { useRouter } from 'vue-router';
import { useTeamMutation } from '@root/composables/useTeam';

const { t } = useI18n({ useScope: 'global' });

interface Props {
  team?: Team | null;
}
const props = defineProps<Props>();
const team = computed(() => props.team);

function isRequired(value: string): string|boolean {
  if (value && value.trim()) {
    return true;
  }
  return t('teams.form.validations.required');
}

interface TeamForm {
  name: string,
  active: boolean,
  remark: string
}
const { handleSubmit, setValues, defineField } = useForm<TeamForm>({
  validationSchema: {
    name: isRequired,
  },
  initialValues: {
    name: '',
    active: true,
    remark: '',
  },
});

const [active] = defineField('active');

watch(team, nv => {
  if (!nv) return;
  setValues({
    name: nv.name,
    active: nv.active,
    remark: nv.remark,
  });
}, { immediate: true });

const router = useRouter();
const goBack = async() => {
  if (router.options.history.state.back) {
    router.go(-1);
  }
  await router.replace({ name: 'club.teams' });
};
const { mutate } = useTeamMutation({
  onSuccess: async() => await goBack(),
});

const errorMessage = ref<string>('');
const onSubmitForm = handleSubmit(async values => {
  errorMessage.value = '';
  const payload: Team = {
    id: team.value?.id,
    name: values.name,
    remark: values.remark,
    active: values.active,
    members: [],
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
    <FormSection :title="t('teams.form.sections.team.title')">
      <template #description>
        {{ t('teams.form.sections.team.description') }}
      </template>
      <FormSectionFields class="bg-white">
        <KwaiInputField
          name="name"
          :required="true"
          :placeholder="t('teams.form.sections.team.fields.name.placeholder')"
        >
          <template #label>
            {{ t('teams.form.sections.team.fields.name.label') }}
          </template>/
        </KwaiInputField>
      </FormSectionFields>
    </FormSection>
    <FormSection :title="t('teams.form.sections.remark.title')">
      <template #description>
        {{ t('teams.form.sections.remark.description') }}
      </template>
      <FormSectionFields class="bg-white">
        <KwaiTextarea
          name="remark"
          :placeholder="t('teams.form.sections.remark.fields.remark.placeholder')"
          :rows="5"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('teams.form.sections.remark.fields.remark.label') }}&nbsp;:
            </span>
          </template>
        </KwaiTextarea>
      </FormSectionFields>
    </FormSection>
    <FormSection>
      <FormSectionFields class="bg-white">
        <KwaiCheckbox
          v-model="active"
        >
          <template #label>
            {{ t('teams.form.sections.submit.fields.active.label') }}
          </template>
        </KwaiCheckbox>
        <div class="flex flex-col items-end mt-6">
          <KwaiButton
            id="submit"
            :method="onSubmitForm"
          >
            {{ t('teams.form.sections.submit.fields.button.label') }}
          </KwaiButton>
        </div>
        <KwaiErrorAlert v-if="errorMessage">
          {{ t('teams.form.error') }}
        </KwaiErrorAlert>
      </FormSectionFields>
    </FormSection>
  </form>
</template>

<style scoped>

</style>
