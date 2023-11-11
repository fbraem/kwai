import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  base: '/author/',
  server: {
    port: 3001,
  },
  plugins: [
    vue(),
  ],
});
