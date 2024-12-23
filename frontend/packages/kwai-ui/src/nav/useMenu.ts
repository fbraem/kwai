import { useRouter } from 'vue-router';
import { computed } from 'vue';
import { MenuItem } from '../types';

/**
 * A composable that returns a MenuItem array based on the routes.
 * When a route has a meta property 'title', it will be added to the list.
 */
export const useMenu = () => {
  const router = useRouter();

  return computed((): MenuItem[] => {
    const result: MenuItem[] = [];
    const routeOrder: Record<string, number> = {};
    let rank = 0;
    for (const route of router.options.routes[0].children || []) {
      if (!route.name) continue;
      routeOrder[route.name as string] = rank++;
    }
    const routes = [];
    for (const route of router.getRoutes()) {
      if (route.meta.title) {
        routes.push(route);
      }
    }
    routes.sort((a, b) => {
      const menuA = routeOrder[a.name as string];
      const menuB = routeOrder[b.name as string];
      if (menuA < menuB) return -1;
      if (menuA > menuB) return 1;
      return 0;
    });
    for (const route of routes) {
      result.push({
        title: route.meta.title as string,
        route,
        disabled: false,
      });
    }
    return result;
  });
};
