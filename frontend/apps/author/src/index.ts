import { createApp } from 'vue';
import App from './App.vue';
import './index.css';

import { VueQueryPlugin } from '@tanstack/vue-query';
import { createRouter, createWebHistory } from 'vue-router';

import routes from './routes';

const app = createApp(App);
app.use(VueQueryPlugin);

const router = createRouter({
  history: createWebHistory(),
  routes: [],
});
routes.forEach(route => router.addRoute(route));
app.use(router);
app.mount('#app');
