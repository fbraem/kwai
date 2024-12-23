import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import toml from '@fbraem/rollup-plugin-toml';
import VueI18nPlugin from '@intlify/unplugin-vue-i18n/vite';

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

export default defineConfig(({ mode }) => {
  return {
    base: '/apps/auth/',
    esbuild: {
      pure: mode === 'production' ? ['console.log'] : [],
    },
    server: {
      origin: 'http://localhost:3002',
      host: '0.0.0.0',
      port: 3002,
    },
    build: {
      manifest: true,
      rollupOptions: {
        input: 'src/index.ts',
      },
    },
    plugins: [
      vue(),
      toml(),
      VueI18nPlugin({
        include: resolve(__dirname, './src/locales/**'),
        compositionOnly: true,
      }),
      visualizer(),
    ],
    resolve: {
      alias: [
        {
          find: '@theme',
          replacement: '',
          customResolver: resolveTheme,
        },
        {
          find: '@kwai/ui',
          replacement: mode === 'production'
            ? '@kwai/ui'
            : resolve(__dirname, '../../packages/kwai-ui/src/'),
        },
        {
          find: /^@root\/(.*)/,
          replacement: `${resolve(__dirname)}/src/$1`,
        },
      ],
    },
  };
});
