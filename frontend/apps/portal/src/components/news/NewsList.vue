<script setup lang="ts">
import { useOffsetPagination } from '@vueuse/core';
import { useNewsItems } from '@root/composables/useNewsItem';
import { computed, ref, watch } from 'vue';
import RightArrowIcon from '@root/components/icons/RightArrowIcon.vue';
import LeftArrowIcon from '@root/components/icons/LeftArrowIcon.vue';
interface Props {
  promoted?: boolean;
  application?: string | null;
}
const props = withDefaults(defineProps<Props>(), {
  promoted: false,
  application: null,
});

const application = props.application ? ref(props.application) : null;

const offset = ref(0);
const limit = ref(10);

const { isLoading, data: newsItems } = useNewsItems({
  promoted: props.promoted,
  application,
  offset,
  limit,
});

const numberOfItems = ref(0);

watch(newsItems, (nv) => {
  if (nv) {
    numberOfItems.value = nv.meta.count;
  }
});

const gotoPage = ({ currentPage } : { currentPage: number }) => {
  offset.value = (currentPage - 1) * limit.value;
};

const {
  currentPage,
  pageCount,
  isFirstPage,
  isLastPage,
  prev,
  next,
} = useOffsetPagination({
  total: numberOfItems,
  page: 1,
  pageSize: 10,
  onPageChange: gotoPage,
  onPageSizeChange: gotoPage,
});

const pages = computed(() => {
  const delta = 4;
  const range = [];
  for (let i = Math.max(2, currentPage.value - delta);
    i <= Math.min(pageCount.value - 1,
      currentPage.value + delta); i++) {
    range.push(i);
  }
  if (currentPage.value - delta > 2) {
    range.unshift('...');
  }
  if (currentPage.value + delta < pageCount.value - 1) {
    range.push('...');
  }

  range.unshift(1);
  range.push(pageCount.value);

  return range;
});
</script>

<template>
  <div>
    <slot
      name="title"
      :loading="isLoading"
    />
    <template v-if="newsItems">
      <template v-if="newsItems.items.length === 0">
        <slot name="empty" />
      </template>
      <template
        v-for="newsItem in newsItems.items"
        v-else
      >
        <slot :news-item="newsItem" />
      </template>
      <nav
        v-if="pageCount > 1"
        class="flex justify-between align-items-center border-t border-gray-200 border-box"
      >
        <div class="flex items-center border-box">
          <span
            v-if="isFirstPage"
            class="inline-flex items-center pt-4 pr-1 font-medium text-sm text-opacity-1 text-gray-400 border-t-2 border-transparent"
          >
            <LeftArrowIcon class="w-4 h-4 fill-current mr-2" /> Vorige
          </span>
          <a
            v-else
            href="#"
            class="inline-flex items-center pt-4 pr-1 font-medium text-sm text-opacity-1 text-gray-500 border-t-2 border-transparent hover:border-t-2 hover:border-t-red-500"
            @click.prevent.stop="prev"
          >
            <LeftArrowIcon class="w-4 h-4 fill-current mr-2" /> Vorige
          </a>
        </div>
        <div class="hidden flex-grow sm:flex justify-center border-box">
          <template
            v-for="page in pages"
            :key="`news-page-${page}`"
          >
            <a
              v-if="typeof page === 'number' && page !== currentPage"
              href="#"
              class="pt-4 px-4 font-medium text-sm text-opacity-1 text-gray-500 border-t-2 border-transparent align-items-center hover:border-t-2 hover:border-t-red-500"
              @click.prevent.stop="currentPage = page"
            >
              {{ page }}
            </a>
            <span
              v-else-if="page === '...'"
              class="pt-4 px-4 font-medium text-sm text-opacity-1 text-gray-500 border-t-2 border-transparent align-items-center"
            >
              ...
            </span>
            <span
              v-else
              class="pt-4 px-4 font-medium text-sm text-opacity-1 text-red-500 border-t-2 border-t-red-500 align-items-center"
            >
              {{ page }}
            </span>
          </template>
        </div>
        <div class="flex items-center border-box">
          <span
            v-if="isLastPage"
            class="inline-flex items-center pt-4 pr-1 font-medium text-sm text-opacity-1 text-gray-400 border-t-2 border-transparent"
          >
            Volgende <RightArrowIcon class="w-4 h-4 fill-current ml-2" />
          </span>
          <a
            v-else
            href="#"
            class="inline-flex items-center pt-4 pl-1 font-medium text-sm text-opacity-1 text-gray-500 border-t-2 border-transparent hover:border-t-2 hover:border-t-red-500 "
            @click.prevent.stop="next"
          >
            Volgende <RightArrowIcon class="w-4 h-4 fill-current ml-2" />
          </a>
        </div>
      </nav>
    </template>
  </div>
</template>
