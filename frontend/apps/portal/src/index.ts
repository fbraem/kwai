import { createApp } from 'vue';

import App from './App.vue';
import './index.css';

import { createRouter, createWebHistory } from 'vue-router';
import routes from './routes';
import { VueQueryPlugin } from '@tanstack/vue-query';

const app = createApp(App);

app.use(VueQueryPlugin);

const router = createRouter({
  history: createWebHistory(),
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

app.mount('#app');
