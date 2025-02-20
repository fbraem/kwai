import { createApp } from 'vue';
// Create app
import App from './App.vue';
import '@root/index.css';

import { init } from '@kwai/ui';
import {
  createRouter, createWebHistory,
} from 'vue-router';
import routes from './routes';
import { VueQueryPlugin } from '@tanstack/vue-query';

const app = createApp(App);

app.use(VueQueryPlugin);

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [],
});
router.beforeEach((to, from, next) => {
  // Redirect if fullPath begins with a hash (ignore hashes later in path)
  if (to.fullPath.substring(0, 2) === '/#') {
    const path = to.fullPath.substring(2);
    next(path);
    return;
  }
  next();
});
routes.forEach(route => router.addRoute(route));
app.use(router);
init(app);

app.config.globalProperties.$kwai = window.__KWAI__;

app.mount('#app');
