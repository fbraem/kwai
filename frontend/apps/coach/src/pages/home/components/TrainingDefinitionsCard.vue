<script setup lang="ts">
import { KwaiCard, ListIcon, KwaiButton } from '@kwai/ui';
import { useI18n } from 'vue-i18n';
const { t } = useI18n({ useScope: 'global' });
</script>

<template>
  <KwaiCard class="w-full">
    <template #title>
      {{ t('home.training_definitions.title') }}
    </template>
    {{ t('home.training_definitions.description') }}
    <template #footer>
      <div class="flex justify-between items-center">
        <KwaiButton
          :to="{ name: 'coach.training_definitions' }"
          small
        >
          <ListIcon
            class="w-4 mr-2 fill-current"
          />
          {{ t('home.training_definitions.list') }}
        </KwaiButton>
      </div>
    </template>
  </KwaiCard>
</template>

<style scoped>

</style>
