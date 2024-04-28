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
