import { defineConfig, splitVendorChunkPlugin } from 'vite';
import vue from '@vitejs/plugin-vue';

import { existsSync } from 'fs';
import { resolve } from 'path';

import { visualizer } from 'rollup-plugin-visualizer';

const resolveTheme = (path: string) => {
  const themeFile = resolve(__dirname, `./src/theme/kwai${path}`);
  // When the theme file exists, use it
  if (existsSync(themeFile)) {
    console.log(`${path} resolved to the theme file ${themeFile}`);
    return themeFile;
  }
  // Otherwise use the default
  const original = resolve(__dirname, `./src${path}`);
  console.log(`No theme file found for ${path}, fallback on ${original}`);
  return original;
};

export default defineConfig(() => {
  return {
    base: '/',
    server: {
      host: '0.0.0.0',
      port: 3000,
    },
    plugins: [
      vue(), splitVendorChunkPlugin(), visualizer(),
    ],
    resolve: {
      alias: [
        {
          find: '@theme',
          replacement: '',
          customResolver: resolveTheme,
        },
        {
          find: /^@root\/(.*)/,
          replacement: `${resolve(__dirname)}/src/$1`,
        },
      ],
    },
    test: {
      global: true,
      environment: 'jsdom',
    },
  };
});
