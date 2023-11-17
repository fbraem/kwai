import { createApp } from 'vue';
// Create app
import App from './App.vue';
import './index.css';

// Setup i18n
import { createI18n } from 'vue-i18n';
import messages from '@intlify/unplugin-vue-i18n/messages';

// Setup pinia store
import { createPinia } from 'pinia';

// Setup router
import { createRouter, createWebHistory } from 'vue-router';
import { routes } from './routes';

const app = createApp(App);
const i18n = createI18n({
  legacy: false,
  locale: 'nl',
  messages,
});
app.use(i18n);

const pinia = createPinia();
app.use(pinia);

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});
app.use(router);

app.mount('#app');
