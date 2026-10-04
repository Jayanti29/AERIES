/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        aeris: {
          bg: '#0B1220',
          surface: '#111A2E',
          raised: '#172238',
          border: '#24304A',
          primary: '#E8EDF7',
          secondary: '#9AA7BF',
          accent: '#3B82F6',
          healthy: '#22A06B',
          warning: '#D99A1B',
          critical: '#E5484D',
          info: '#4C9AFF',
          unknown: '#7A869C'
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      }
    },
  },
  plugins: [],
}
