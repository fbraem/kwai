<script setup lang="ts">
import { useOffsetPagination } from '@vueuse/core';
import { computed, ref } from 'vue';
import RightArrowIcon from '../icons/RightArrowIcon.vue';
import LeftArrowIcon from '../icons/LeftArrowIcon.vue';
interface Props {
  page: number
  itemsCount: number
  limit: number
}
const props = defineProps<Props>();
const page = ref(props.page);
const itemsCount = ref(props.itemsCount);
const limit = ref(props.limit);

const emit = defineEmits<{
  (e: 'changePage', newPage: number): void
}>();
const gotoPage = ({ currentPage } : { currentPage: number }) => {
  emit('changePage', currentPage);
};

const {
  currentPage,
  pageCount,
  isFirstPage,
  isLastPage,
  prev,
  next,
} = useOffsetPagination({
  total: itemsCount,
  page,
  pageSize: limit,
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
