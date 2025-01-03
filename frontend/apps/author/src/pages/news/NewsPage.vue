<script setup lang="ts">
import {
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
  NewIcon,
  CancelIcon,
  CheckIcon,
  EditIcon,
  KwaiButton,
  KwaiToolbar,
  OffsetPagination,
  usePagination,
} from '@kwai/ui';

import { useNewsItems } from '@root/composables/useNewsItem';
import { useI18n } from 'vue-i18n';
import PromotedIcon from '@root/components/icons/PromotedIcon.vue';

const { t } = useI18n({ useScope: 'global' });

const { offset, limit, currentPage, changePage } = usePagination({ limit: 10 });
const { data: newsItems } = useNewsItems({
  offset, limit,
});
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>{{ t('news.home.title') }}</ContainerSectionTitle>
    <ContainerSectionContent>
      <KwaiToolbar
        start-class="w-full sm:w-1/2"
        end-class="w-full sm:w-1/3 sm:place-content-end"
      >
        <template #start>
          <div class="flex flex-col">
            <h5 class="mr-3 font-semibold">
              {{ t('news.home.toolbar.title') }}
            </h5>
            <p class="text-gray-500">
              {{ t('news.home.toolbar.description') }}
            </p>
          </div>
        </template>
        <template #end>
          <KwaiButton :to="{ name: 'author.news.create' }">
            <NewIcon class="w-4 mr-2 fill-current" />
            {{ t('news.home.toolbar.button') }}
          </KwaiButton>
        </template>
      </KwaiToolbar>
      <div
        v-if="newsItems"
        class="relative w-full overflow-x-auto"
      >
        <table class="w-full text-sm text-left rtl:text-right">
          <thead class="text-xs text-gray-700 uppercase bg-gray-50">
            <tr>
              <th
                scope="col"
                class="px-6 py-3"
              >
                {{ t('news.home.table.columns.title') }}
              </th>
              <th
                scope="col"
                class="px-6 py-3"
              >
                {{ t('news.home.table.columns.application') }}
              </th>
              <th
                scope="col"
                class="px-6 py-3"
              >
                {{ t('news.home.table.columns.state') }}
              </th>
              <th
                scope="col"
                class="px-6 py-3"
              />
            </tr>
          </thead>
          <tbody>
            <template
              v-for="newsItem in newsItems.items"
              :key="newsItem.id"
            >
              <tr>
                <th
                  scope="row"
                  class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap flex items-center"
                >
                  {{ newsItem.texts[0].title }}
                  <PromotedIcon
                    v-if="newsItem.priority > 0"
                    class="ml-2 w-4 fill-yellow-400"
                  />
                </th>
                <td class="px-6 py-4">
                  {{ newsItem.application.title }}
                </td>
                <td
                  class="px-6 py-4"
                  rowspan="2"
                >
                  <CheckIcon
                    v-if="newsItem.enabled"
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
                  <KwaiButton :to="{ name: 'author.news.edit', params: { id: newsItem.id } }">
                    <EditIcon class="w-4 fill-current" />
                  </KwaiButton>
                </td>
              </tr>
              <tr class="border-b">
                <td
                  class="px-6 pb-4 text-xs text-gray-500"
                  colspan="2"
                >
                  <div v-html="newsItem.texts[0].summary" />
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
      <OffsetPagination
        v-if="newsItems"
        :page="currentPage"
        :items-count="newsItems.meta.count"
        :limit="limit"
        @change-page="(newPage) => changePage(newPage)"
      />
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
