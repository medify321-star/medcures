/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: 'rgb(11 15 23)',
        foreground: 'rgb(248 250 252)',
        primary: 'rgb(56 189 248)',
        secondary: 'rgb(45 212 191)',
        muted: 'rgb(100 116 139)',
      },
      animation: {
        'in': 'fadeIn 0.7s ease-in-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
