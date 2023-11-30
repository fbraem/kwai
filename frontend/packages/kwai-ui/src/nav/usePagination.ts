import { ref, toRef } from 'vue';
import type { Ref } from 'vue';

interface PaginationOptions {
  limit: number | Ref<number>,
}

export const usePagination = (options: PaginationOptions = { limit: 10 }) => {
  const offset = ref(0);
  const limit = toRef(options.limit);
  const currentPage = ref(1);
  const changePage = (newPage: number) => {
    currentPage.value = newPage;
    offset.value = (newPage - 1) * limit.value;
  };
  return {
    offset,
    limit,
    currentPage,
    changePage,
  };
};
