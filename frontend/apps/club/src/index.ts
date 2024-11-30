import { createApp } from 'vue';
import App from './App.vue';
import './index.css';
import './style.css';

import { VueQueryPlugin } from '@tanstack/vue-query';
import { createRouter, createWebHistory } from 'vue-router';

// Setup i18n
import { createI18n } from 'vue-i18n';
import messages from '@intlify/unplugin-vue-i18n/messages';

import routes from './routes';
import { localStorage } from '@kwai/api';

import { init } from '@kwai/ui';

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

declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean
  }
 }

router.beforeEach((to, from, next) => {
  const requiresAuth: boolean = to.meta.requiresAuth ?? true; // By default, all routes need authentication
  if (requiresAuth) {
    if (localStorage.refreshToken.value == null) {
      localStorage.loginRedirect.value = `/apps/club${to.path}`;
      next('/not_allowed');
    } else {
      next(); // Already logged in
    }
  } else {
    next(); // Login not needed
  }
});
app.use(router);
init(app);

app.mount('#app');
