import { useRouter } from 'vue-router';
import { computed } from 'vue';
import { MenuItem } from '../../dist';

export const useMenu = () => {
  const router = useRouter();

  return computed((): MenuItem[] => {
    const result: MenuItem[] = [];
    for (const route of router.getRoutes()) {
      if (route.meta.title) {
        result.push({
          title: route.meta.title as string,
          route,
        });
      }
    }
    return result;
  });
};
