// Used for custom styles in templates

tailwind.config = {
      theme: {
        extend: {
          borderWidth: {
            '12': '12px',
          },
          keyframes: {
            slideIn: {
              '0%': { transform: 'translateX(-100%)' },
              '100%': { transform: 'translateX(0)' },
            },
            levelBarSlideIn: {
                from: { width: '0' },
                to: { width: '100%' },
            }
          },
          animation: {
            slideIn: 'slideIn 0.3s ease-in-out',
            levelBarSlideIn: 'levelBarSlideIn 0.9s ease-in-out'
          },
        },
      },
}