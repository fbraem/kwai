import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

import { existsSync } from 'fs';
import { resolve } from 'path';

import { visualizer } from 'rollup-plugin-visualizer';
import { ViteToml } from 'vite-plugin-toml';

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

export default defineConfig(({ mode }) => {
  return {
    base: '/apps/portal/',
    server: {
      origin: 'http://localhost:3000',
      host: '0.0.0.0',
      port: 3000,
    },
    build: {
      manifest: true,
      rollupOptions: { input: 'src/index.ts' },
    },
    plugins: [ViteToml(), vue(), visualizer()],
    resolve: {
      alias: [
        {
          find: '@kwai/ui',
          replacement:
            mode === 'production'
              ? '@kwai/ui'
              : resolve(__dirname, '../../packages/kwai-ui/src/'),
        },
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
