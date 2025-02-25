import type {
  LocationAsRelativeRaw, RouteRecord,
} from 'vue-router';

export interface ApiError {
  status: string
  message: string
  url: string
}

export interface MenuItem {
  title: string
  route?: RouteRecord | LocationAsRelativeRaw
  url?: string
  method?: () => void
  disabled?: boolean
}
