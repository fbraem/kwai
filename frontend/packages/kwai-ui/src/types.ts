import type { LocationAsRelativeRaw, RouteRecord } from 'vue-router';

export interface MenuItem {
  title: string,
  route?: RouteRecord | LocationAsRelativeRaw,
  url?: string,
  method?: () => void
}
