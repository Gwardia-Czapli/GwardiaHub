from django import template

register = template.Library()


@register.filter
def calculate_percentage(value, arg):
    return str((float(value) / float(arg)) * 100).replace(",", ".")
