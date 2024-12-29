<script setup lang="ts">
import { KwaiCard, KwaiButton, ListIcon } from '@kwai/ui';
import { useI18n } from 'vue-i18n';
const { t } = useI18n({ useScope: 'global' });
</script>

<template>
  <KwaiCard class="w-full">
    <template #title>
      {{ t('home.trainings.title') }}
    </template>
    {{ t('home.trainings.description') }}
    <template #footer>
      <div class="flex justify-between items-center">
        <KwaiButton
          :to="{ name: 'coach.trainings' }"
          small
        >
          <ListIcon
            class="w-4 mr-2 fill-current"
          />
          {{ t('home.trainings.list') }}
        </KwaiButton>
      </div>
    </template>
  </KwaiCard>
</template>

<style scoped>

</style>
