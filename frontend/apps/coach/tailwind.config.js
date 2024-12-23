/** @type {import('tailwindcss').Config} */
import primeui from 'tailwindcss-primeui';

module.exports = {
  content: [
    './index.html',
    './src/**/*.{html,js,ts,vue,jsx,tsx}',
    '../../packages/kwai-ui/src/**/*.{html,js,ts,vue,jsx,tsx}',
  ],
  theme: {
    extend: {
    },
  },
  plugins: [primeui],
};
