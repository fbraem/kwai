<script setup lang="ts">
import {
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
  NewIcon,
  CancelIcon,
  CheckIcon,
  EditIcon,
  OffsetPagination,
  usePagination,
} from '@kwai/ui';

import { useNewsItems } from '@root/composables/useNewsItem';
import PrimaryButton from '@root/components/PrimaryButton.vue';
import { useI18n } from 'vue-i18n';
import PromotedIcon from '@root/components/icons/PromotedIcon.vue';

const { t } = useI18n({ useScope: 'global' });

const { offset, limit, page, changePage } = usePagination({ limit: 10 });
const { data: newsItems } = useNewsItems({ offset, limit });
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>{{ t('news.home.title') }}</ContainerSectionTitle>
    <ContainerSectionContent>
      <div class="w-full max-w-screen-xl mx-auto">
        <div class="relative overflow-hidden bg-white shadow-md sm:rounded-lg">
          <div class="flex-row items-center justify-between p-4 space-y-3 sm:flex sm:space-y-0 sm:space-x-4">
            <div>
              <h5 class="mr-3 font-semibold">
                {{ t('news.home.toolbar.title') }}
              </h5>
              <p class="text-gray-500">
                {{ t('news.home.toolbar.description') }}
              </p>
            </div>
            <PrimaryButton
              :route="{ name: 'author.news.create' }"
              class="flex items-center"
            >
              <NewIcon class="w-4 mr-2 fill-current" />
              {{ t('news.home.toolbar.button') }}
            </PrimaryButton>
          </div>
        </div>
      </div>
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
                  <router-link
                    :to="{ name: 'author.news.edit', params: { id: newsItem.id } }"
                    class="border-none text-base inline-flex justify-center items-center align-middle no-underline rounded-full cursor-pointer focus:outline-none hover:no-underline hover:bg-yellow-300 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed p-2"
                  >
                    <EditIcon class="w-4 fill-current" />
                  </router-link>
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
        :page="page"
        :items-count="newsItems.meta.count"
        :limit="limit"
        @change-page="(newPage) => changePage(newPage)"
      />
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
