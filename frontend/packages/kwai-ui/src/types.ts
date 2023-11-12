import type { RouteRecord } from 'vue-router';

export interface MenuItem {
  title: string,
  route?: RouteRecord,
  url?: string,
  method?: () => void
}
