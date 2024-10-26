import './index.css';
import { App } from 'vue';
import Kwai from './presets/kwai';
import PrimeVue from 'primevue/config';
export type { MenuItem } from './types';
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

export const init = (app: App) => {
  app.use(PrimeVue, { unstyled: true, pt: Kwai });
};
