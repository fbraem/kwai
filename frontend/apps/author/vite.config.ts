import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';

export default defineConfig({
  base: '/',
  server: {
    host: '0.0.0.0',
    port: 3001,
  },
  plugins: [
    vue(),
  ],
  resolve: {
    alias: [
      {
        find: /^@root\/(.*)/,
        replacement: `${resolve(__dirname)}/src/$1`,
      },
    ],
  },
});
