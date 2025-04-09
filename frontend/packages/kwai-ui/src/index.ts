import { App } from 'vue';
import PrimeVue from 'primevue/config';
import './index.css';

export type { ApiError, MenuItem } from './types';
export * from './alerts';
export * from './badges';
export * from './card';
export * from './dialogs';
export * from './icons';
export * from './form';
export type * from './form';
export * from './layout';
export * from './nav';
export * from './section';
export * from './table';
export * from './validations';
export { default as KwaiLoadBoundary } from './KwaiLoadBoundary.vue';

export const init = (app: App) => {
  app.use(PrimeVue, { theme: 'none' });
};
