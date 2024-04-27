// Not used in code! Only for PyCharm to recognize Tailwind usage

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [],
  theme: {
    extend: {
      borderWidth: {
        '12': '12px',
      },
      keyframes: {
        slideIn: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(0)' },
        }
      },
      animation: {
        slideIn: 'slideIn 0.3s ease-in-out'
      },
    },
  },
  plugins: [],
}

