import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';
import VueI18nPlugin from '@intlify/unplugin-vue-i18n/vite';

export default defineConfig(({ mode }) => {
  return {
    base: mode === 'development' ? '/coach/' : '/',
    esbuild: {
      pure: mode === 'production' ? ['console.log'] : [],
    },
    server: {
      host: '0.0.0.0',
      port: 3003,
    },
    plugins: [
      vue(),
      VueI18nPlugin({
        include: resolve(__dirname, './src/locales/**'),
        compositionOnly: true,
      }),
    ],
    resolve: {
      alias: [
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
      dedupe: ['vue'],
    },
    test: {
      global: true,
      environment: 'jsdom',
    },
  };
});
