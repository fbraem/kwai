import {defineConfig} from "vite";
import {resolve} from 'path';
import dts from 'vite-plugin-dts';

export default defineConfig({
  plugins: [
    dts({tsconfigPath: './tsconfig.json'}),
  ],
  build: {
    lib: {
      entry: resolve(__dirname, 'src/index.ts'),
      name: '@kwai/date',
      fileName: 'kwai-date',
    },
  },
});
