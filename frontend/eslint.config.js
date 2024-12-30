import stylistic from '@stylistic/eslint-plugin';
import pluginVue from 'eslint-plugin-vue';
import vueTsEslintConfig from '@vue/eslint-config-typescript';

export default [
  {
    files: [
      'apps/**/*.{js,jsx,ts,tsx,vue}',
      'packages/**/*.{js,jsx,ts,tsx,vue}',
    ],
  },
  {
    ignores: [
      '**/dist',
      'node_modules/**',
    ],
  },
  stylistic.configs['recommended-flat'],
  ...pluginVue.configs['flat/strongly-recommended'],
  ...vueTsEslintConfig(),
  {
    rules: {
      '@stylistic/comma-dangle': ['error', {
        arrays: 'always-multiline',
        objects: 'always-multiline',
        imports: 'always-multiline',
        exports: 'always-multiline',
        functions: 'never',
      }],
      '@stylistic/indent': ['error', 2],
      '@stylistic/object-property-newline': ['error', { allowAllPropertiesOnSameLine: true }],
      '@stylistic/quotes': ['error', 'single'],
      '@stylistic/quote-props': ['error', 'as-needed'],
      '@stylistic/semi': ['error', 'always'],
      '@stylistic/space-before-function-paren': ['error', 'never'],
      'vue/block-order': ['error', {
        order: ['script', 'template', 'style'],
      }],
      'vue/max-attributes-per-line': ['error', {
        singleline: {
          max: 1,
        },
        multiline: {
          max: 1,
        },
      }],
      'vue/one-component-per-file': 'off',
    },
  },
];
