// Used for custom styles in templates

tailwind.config = {
      theme: {
        extend: {
          borderWidth: {
            '12': '12px',
          },
          keyframes: {
            levelBarSlideIn: {
                from: { width: '0' },
                to: { width: '100%' },
            }
          },
          animation: {
            levelBarSlideIn: 'levelBarSlideIn 0.9s ease-in-out'
          },
        },
      },
}