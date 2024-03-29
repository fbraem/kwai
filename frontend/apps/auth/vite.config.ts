import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import toml from '@fbraem/rollup-plugin-toml';
import VueI18nPlugin from '@intlify/unplugin-vue-i18n/vite';

import { existsSync } from 'fs';
import { resolve } from 'path';

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

export default defineConfig({
  base: '/auth/',
  server: {
    port: 3002,
  },
  plugins: [
    vue(),
    toml(),
    VueI18nPlugin({
      include: resolve(__dirname, './src/locales/**'),
      compositionOnly: true,
    }),
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
});
