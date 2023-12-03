import { createApp } from 'vue';
import App from '@root/App.vue';
import '@root/index.css';
import '@kwai/ui/index.css';

import { createRouter, createWebHistory } from 'vue-router';
import routes from '@root/routes';

import { createI18n } from 'vue-i18n';
import messages from '@intlify/unplugin-vue-i18n/messages';

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

app.mount('#app');
