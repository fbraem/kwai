import toml from '@fbraem/rollup-plugin-toml';
import dts from 'vite-plugin-dts';
import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig(({ mode }) => {
  const configFile = mode === 'production' ? 'src/config.production.toml' : 'src/config.toml';
  return {
    plugins: [
      toml(),
      dts({ copyDtsFiles: true }),
    ],
    build: {
      lib: {
        entry: resolve(__dirname, configFile),
        name: '@kwai/config',
        fileName: 'kwai-config',
      },
      rollupOptions: {
        output: {
          exports: 'named',
        },
      },
    },
  };
});
