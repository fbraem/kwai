/** @type {import('tailwindcss').Config} */
import TailwindForms from '@tailwindcss/forms';
import primeui from 'tailwindcss-primeui';

export default {
  content: [
    './index.ts',
    './src/**/*.{html,js,ts,vue,jsx,tsx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [
    TailwindForms(), primeui,
  ],
};
