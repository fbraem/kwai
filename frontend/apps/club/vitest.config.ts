import { resolve } from 'path';
import { loadEnv } from 'vite';
import { defineConfig } from 'vitest/config';

export default defineConfig(({ mode }) => ({
  test: {
    globals: true,
    environment: 'jsdom',
    env: loadEnv(mode, '../../', ''),
  },
  resolve: {
    alias: [
      {
        find: /^@root\/(.*)/,
        replacement: `${resolve(__dirname)}/src/$1`,
      },
    ],
  },
}));
