import { useRouter } from 'vue-router';
import { computed } from 'vue';
import { MenuItem } from '../../dist';

/**
 * A composable that returns a MenuItem array based on the routes.
 * When a route has a meta property 'title', it will be added to the list.
 */
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
