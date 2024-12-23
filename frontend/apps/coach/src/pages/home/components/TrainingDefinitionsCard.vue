<script setup lang="ts">
import { Card, CardTitle, ListIcon, KwaiButton } from '@kwai/ui';
import { useI18n } from 'vue-i18n';
const { t } = useI18n({ useScope: 'global' });
</script>

<template>
  <Card class="w-full">
    <template #header>
      <CardTitle class="p-3 font-bold text-lg text-gray-900">
        {{ t('home.training_definitions.title') }}
      </CardTitle>
    </template>
    <p class="p-3">
      {{ t('home.training_definitions.description') }}
    </p>
    <template #footer>
      <div class="flex justify-between items-center p-3">
        <KwaiButton :to="{ name: 'coach.training_definitions' }">
          <ListIcon
            class="w-4 mr-2 fill-current"
          />
          {{ t('home.training_definitions.list') }}
        </KwaiButton>
      </div>
    </template>
  </Card>
</template>

<style scoped>

</style>
