import js from '@eslint/js';
import ts from 'typescript-eslint';
import pluginVue from 'eslint-plugin-vue';
import eslintConfigPrettier from 'eslint-config-prettier';

export default [
  {
    files: [
      'apps/**/*.{js,jsx,ts,tsx}',
      'packages/**/*.{js,jsx,ts,tsx}',
    ],
    ignores: [
      '**/dist',
      'node_modules/**',
    ],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "module",
    }
  },
  js.configs.recommended,
  ...ts.configs.recommended,
  ...pluginVue.configs['flat/strongly-recommended'],
  {
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      parserOptions: {
        parser: ts.parser,
        extraFileExtensions: ['.vue'],
      }
    }
  },
  {
    rules: {
      semi: [2, 'always'],
      'comma-dangle': ['error', {
        arrays: 'always-multiline',
        objects: 'always-multiline',
        imports: 'always-multiline',
        exports: 'always-multiline',
        functions: 'never',
      }],
      'space-before-function-paren': [2, 'never'],
      'vue/block-order': ['error', {
        'order': [ 'script', 'template', 'style' ],
      }],
    }
  },
  eslintConfigPrettier
];
