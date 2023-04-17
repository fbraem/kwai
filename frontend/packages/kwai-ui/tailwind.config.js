/** @type {import('tailwindcss').Config} */
import TailwindForms from "@tailwindcss/forms"

export default {
    content: [
        "./index.ts",
        "./src/**/*.{html,js,ts,vue,jsx,tsx}"
    ],
    theme: {
        extend: {},
    },
    plugins: [
        TailwindForms()
    ],
}
