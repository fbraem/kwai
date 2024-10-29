/** @type {import('tailwindcss').Config} */
import colors from 'tailwindcss/colors';
module.exports = {
  content: [
    './index.html',
    './src/**/*.{html,js,ts,vue,jsx,tsx}',
    '../../packages/kwai-ui/src/**/*.{html,js,ts,vue,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: colors.yellow['50'],
          100: colors.yellow['100'],
          200: colors.yellow['200'],
          300: colors.yellow['300'],
          400: colors.yellow['400'],
          500: colors.yellow['400'],
          600: colors.yellow['300'],
          700: colors.yellow['500'],
          800: colors.yellow['600'],
          900: colors.yellow['700'],
        },
        'primary-text': colors.white,
      },
    },
  },
  plugins: [],
};
