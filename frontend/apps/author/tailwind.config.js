/** @type {import('tailwindcss').Config} */
import colors from 'tailwindcss/colors';
module.exports = {
  content: [
    './src/**/*.{html,js,ts,vue,jsx,tsx}',
    '../../packages/kwai-ui/src/**/*.{html,js,ts,vue,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: colors.yellow,
        'primary-text': colors.white,
      },
    },
  },
  plugins: [],
};
