import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import dts from 'vite-plugin-dts';
import { resolve } from 'path';

export default defineConfig({
  plugins: [
    vue(),
    dts({ rollupTypes: true }),
  ],
  build: {
    lib: {
      entry: resolve(__dirname, 'src/index.ts'),
      name: '@kwai/ui',
      fileName: 'kwai-ui',
    },
    rollupOptions: {
      // make sure to externalize deps that shouldn't be bundled into the library
      external: ['vue', 'vue-router', 'vee-validate'],
      output: {
        // Provide global variables to use in the UMD build
        // for externalized deps
        globals: {
          vue: 'Vue',
          'vue-router': 'VueRouter',
          'vee-validate': 'VeeValidate',
        },
      },
    },
  },
});
