<script setup lang="ts">
import { useI18n } from 'vue-i18n';

import {
  FormSection,
  FormSectionFields,
  KwaiButton,
  KwaiErrorAlert,
  KwaiInputField,
  TextareaField,
} from '@kwai/ui';
import {
  useUserInvitationMutation, type UserInvitation,
} from '@root/composables/useUserInvitations.ts';
import {
  ref,
  toRef, watch,
} from 'vue';
import { useRouter } from 'vue-router';
import UserInvitationForm from '@root/pages/users/components/UserInvitationForm.vue';
import { useForm } from 'vee-validate';

interface Props {
  userInvitation?: UserInvitation
}
const props = defineProps<Props>();
const userInvitation = toRef(() => props.userInvitation);

const { t } = useI18n({ useScope: 'global' });

function isRequired(value: string): string | boolean {
  if (value && value.trim()) {
    return true;
  }
  return t('user_invitations.form.validations.required');
}

function isEmail(value: string): string | boolean {
  const regex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i;
  if (!regex.test(value)) {
    return t('user_invitations.form.validations.invalid_email');
  }
  return true;
}

interface UserInvitationForm {
  email: string
  firstname: string
  lastname: string
  remark: string
}
const { handleSubmit, setValues } = useForm<UserInvitationForm>({
  validationSchema: {
    email: [isRequired, isEmail],
    firstname: isRequired,
    lastname: isRequired,
  },
  initialValues: {
    email: '',
    firstname: '',
    lastname: '',
    remark: '',
  },
});
watch(userInvitation, (nv) => {
  if (!nv) return;
  setValues({
    email: nv.email,
    firstname: nv.firstname,
    lastname: nv.lastname,
    remark: nv.remark,
  });
}, { immediate: true });

const router = useRouter();
const goBack = async() => {
  if (router.options.history.state.back) {
    router.go(-1);
  }
  await router.replace({ name: 'admin.user_invitations' });
};
const { mutate } = useUserInvitationMutation({ onSuccess: async() => await goBack() });

const errorMessage = ref('');
const onSubmitForm = handleSubmit(async(values) => {
  console.log(values);
  errorMessage.value = '';
  const payload: UserInvitation = {
    id: userInvitation.value?.id,
    email: values.email,
    firstname: values.firstname,
    lastname: values.lastname,
    remark: values.remark,
  };
  mutate(payload, {
    onError: (error) => {
      errorMessage.value = error.message;
    },
  });
});
</script>

<template>
  <form class="w-full bg-surface-100 rounded-lg p-3 grid gap-3">
    <FormSection :title="t('user_invitations.form.sections.user.title')">
      <template #description>
        {{ t('user_invitations.form.sections.user.description') }}
      </template>
      <FormSectionFields class="bg-surface-0">
        <KwaiInputField
          name="email"
          type="email"
          :placeholder="t('user_invitations.form.sections.user.fields.email.placeholder')"
          class="pb-6"
          :required="true"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('user_invitations.form.sections.user.fields.email.label') }} :
            </span>
          </template>
        </KwaiInputField>
        <KwaiInputField
          name="firstname"
          :placeholder="t('user_invitations.form.sections.user.fields.firstname.placeholder')"
          class="pb-6"
          :required="true"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('user_invitations.form.sections.user.fields.firstname.label') }} :
            </span>
          </template>
        </KwaiInputField>
        <KwaiInputField
          name="lastname"
          :placeholder="t('user_invitations.form.sections.user.fields.lastname.placeholder')"
          class="pb-6"
          :required="true"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('user_invitations.form.sections.user.fields.lastname.label') }} :
            </span>
          </template>
        </KwaiInputField>
      </FormSectionFields>
    </FormSection>
    <FormSection :title="t('user_invitations.form.sections.remark.title')">
      <template #description>
        {{ t('user_invitations.form.sections.remark.description') }}
      </template>
      <FormSectionFields class="bg-white">
        <TextareaField
          name="remark"
          :placeholder="t('user_invitations.form.sections.remark.fields.remark.placeholder')"
          :rows="5"
        >
          <template #label>
            <span class="font-medium text-gray-900">
              {{ t('user_invitations.form.sections.remark.fields.remark.label') }}&nbsp;:
            </span>
          </template>
        </TextareaField>
      </FormSectionFields>
    </FormSection>
    <FormSection>
      <FormSectionFields class="bg-surface-0">
        <div>
          {{ t('user_invitations.form.sections.submit.help') }}
        </div>
        <div class="flex flex-col items-end mt-6">
          <KwaiButton
            id="submit"
            :method="onSubmitForm"
          >
            {{ t('user_invitations.form.sections.submit.fields.button.label') }}
          </KwaiButton>
        </div>
        <KwaiErrorAlert v-if="errorMessage">
          {{ t('user_invitations.form.error') }}
        </KwaiErrorAlert>
      </FormSectionFields>
    </FormSection>
  </form>
</template>

<style scoped>

</style>
