import { createApp } from 'vue';

import App from './App.vue';
import './index.css';

import { createPinia } from 'pinia';
import { createRouter, createWebHistory } from 'vue-router';
import routes from './routes';

const pinia = createPinia();
const app = createApp(App);
app.use(pinia);

const router = createRouter({
  history: createWebHistory(),
  routes: [],
});
routes.forEach(route => router.addRoute(route));
app.use(router);

app.mount('#app');
