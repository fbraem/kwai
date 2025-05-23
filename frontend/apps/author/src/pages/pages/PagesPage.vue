<script setup lang="ts">
import { usePages } from '@root/composables/usePage';
import {
  usePagination,
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
  NewIcon,
  EditIcon,
  CheckIcon,
  CancelIcon,
  OffsetPagination,
  KwaiButton,
  KwaiToolbar,
} from '@kwai/ui';
import { useI18n } from 'vue-i18n';

const { t } = useI18n({ useScope: 'global' });

const { offset, limit, currentPage, changePage } = usePagination({ limit: 10 });

const { data: pages } = usePages({
  offset, limit,
});
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>{{ t('pages.home.title') }}</ContainerSectionTitle>
    <ContainerSectionContent>
      <KwaiToolbar
        start-class="w-full sm:w-1/2"
        end-class="w-full sm:w-1/3 sm:place-content-end"
      >
        <template #start>
          <div class="flex flex-col">
            <h5 class="font-semibold">
              {{ t('pages.home.toolbar.title') }}
            </h5>
            <p class="text-gray-500">
              {{ t('pages.home.toolbar.description') }}
            </p>
          </div>
        </template>
        <template #end>
          <KwaiButton :to="{ name: 'author.pages.create' }">
            <NewIcon class="w-4 mr-2 fill-current" />
            {{ t('pages.home.toolbar.button') }}
          </KwaiButton>
        </template>
      </KwaiToolbar>
      <div
        v-if="pages"
        class="relative w-full overflow-x-auto"
      >
        <table class="w-full text-sm text-left rtl:text-right">
          <thead class="text-xs text-gray-700 uppercase bg-gray-50">
            <tr>
              <th
                scope="col"
                class="px-6 py-3"
              >
                {{ t('pages.home.table.columns.title') }}
              </th>
              <th
                scope="col"
                class="px-6 py-3"
              >
                {{ t('pages.home.table.columns.application') }}
              </th>
              <th
                scope="col"
                class="px-6 py-3"
              >
                {{ t('pages.home.table.columns.state') }}
              </th>
              <th
                scope="col"
                class="px-6 py-3"
              />
            </tr>
          </thead>
          <tbody>
            <template
              v-for="page in pages.items"
              :key="page.id"
            >
              <tr>
                <th
                  scope="row"
                  class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap flex items-center"
                >
                  {{ page.texts[0].title }}
                </th>
                <td class="px-6 py-4">
                  {{ page.application.title }}
                </td>
                <td
                  class="px-6 py-4"
                  rowspan="2"
                >
                  <CheckIcon
                    v-if="page.enabled"
                    class="w-4 fill-green-600 font-bold"
                  />
                  <CancelIcon
                    v-else
                    class="w-f4 fill-red-500 font-bold"
                  />
                </td>
                <td
                  class="px-6 py-4"
                  rowspan="2"
                >
                  <KwaiButton :to="{ name: 'author.pages.edit', params: { id: page.id } }">
                    <EditIcon class="w-4 fill-current" />
                  </KwaiButton>
                </td>
              </tr>
              <tr class="border-b">
                <td
                  class="px-6 pb-4 text-xs text-gray-500"
                  colspan="2"
                >
                  <div v-html="page.texts[0].summary" />
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
      <OffsetPagination
        v-if="pages"
        :page="currentPage"
        :items-count="pages.meta.count"
        :limit="limit"
        @change-page="(newPage) => changePage(newPage)"
      />
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
