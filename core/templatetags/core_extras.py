from django import template

register = template.Library()


@register.filter
def calculate_percentage(value, arg):
    try:
        return str((float(value) / float(arg)) * 100).replace(",", ".")
    except (ValueError, ZeroDivisionError):
        return "Invalid input"
