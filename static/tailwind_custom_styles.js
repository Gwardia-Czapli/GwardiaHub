// Used for custom styles in templates

tailwind.config = {
    theme: {
        extend: {
            borderWidth: {
                '12': '12px',
            },
            width: {
                "1/8": "12.5%",
            },
            keyframes: {
                levelBarSlideIn: {
                    '0%': { transform: 'translateX(-100%)' },
                    '100%': { transform: 'translateX(0)' },
                }
            },
            animation: {
                levelBarSlideIn: 'levelBarSlideIn 0.9s ease-in-out'
            },
        },
      },
}
