<script setup lang="ts">
import {
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
  KwaiButton,
  KwaiCard,
  ListIcon,
} from '@kwai/ui';

import { useI18n } from 'vue-i18n';
import InviteUserIcon from '@root/components/icons/InviteUserIcon.vue';

const { t } = useI18n({ useScope: 'global' });
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>
      {{ t('home.description') }}
    </ContainerSectionTitle>
    <ContainerSectionContent>
      <KwaiCard class="w-full">
        <template #title>
          {{ t('home.users.title') }}
        </template>
        {{ t('home.users.description') }}
        <template #footer>
          <div class="flex flex-row justify-between">
            <div>
              <KwaiButton
                :to="{ name: 'admin.users' }"
                small
              >
                <ListIcon class="w-4 mr-2 fill-current" />
                {{ t('home.users.list') }}
              </KwaiButton>
            </div>
            <div>
              <KwaiButton
                :to="{ name: 'admin.user_invitations' }"
                small
              >
                <InviteUserIcon class="w-4 mr-2 fill-current" />
                {{ t('home.user_invitations') }}
              </KwaiButton>
            </div>
          </div>
        </template>
      </KwaiCard>
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped></style>
