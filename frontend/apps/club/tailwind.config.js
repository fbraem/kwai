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
        primary: colors.green,
        'primary-text': colors.white,
      },
    },
  },
  plugins: [],
};
