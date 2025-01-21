/**
 * This files defines the global $kwai variable.
 */
export {};

interface KwaiConfig {
  website: {
    name: string
  }
  contact?: {
    street: string
    city: string
    email: string
  }
  copyright?: string
  admin?: {
    name: string
    email: string
  }
}

declare global {
  interface Window {
    __KWAI__: KwaiConfig
  }
}

declare module 'vue' {
  interface ComponentCustomProperties {
    $kwai: KwaiConfig
  }
}
