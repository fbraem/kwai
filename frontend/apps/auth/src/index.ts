import { createApp } from 'vue';
// Create app
import App from './App.vue';
import '@root/index.css';

// Setup i18n
import { createI18n } from 'vue-i18n';
import messages from '@intlify/unplugin-vue-i18n/messages';

import { init } from '@kwai/ui';

// Setup router
import {
  createRouter, createWebHistory,
} from 'vue-router';
import { routes } from './routes';

const app = createApp(App);
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
