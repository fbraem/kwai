import { createApp } from 'vue';

import App from './App.vue';
import '@root/index.css';

import { createI18n } from 'vue-i18n';
import messages from '@intlify/unplugin-vue-i18n/messages';

import { init } from '@kwai/ui';

import {
  createRouter, createWebHistory,
} from 'vue-router';
import { routes } from './routes';

import { VueQueryPlugin } from '@tanstack/vue-query';

const app = createApp(App);

app.use(VueQueryPlugin);

const i18n = createI18n({
  legacy: false,
  locale: 'nl',
  messages,
});
app.use(i18n);

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});
app.use(router);
init(app);

app.config.globalProperties.$kwai = window.__KWAI__;

app.mount('#app');
