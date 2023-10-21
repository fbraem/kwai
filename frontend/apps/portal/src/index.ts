import { createApp } from 'vue';

import App from './App.vue';
import './index.css';

import { createPinia } from 'pinia';
import { createRouter, createWebHistory } from 'vue-router';
import routes from './routes';
import { VueQueryPlugin } from '@tanstack/vue-query';

const pinia = createPinia();
const app = createApp(App);
app.use(pinia);

app.use(VueQueryPlugin);

const router = createRouter({
  history: createWebHistory(),
  routes: [],
});
routes.forEach(route => router.addRoute(route));
app.use(router);

app.mount('#app');
