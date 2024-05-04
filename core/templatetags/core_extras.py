from django import template

register = template.Library()


@register.filter
def calculate_percentage(value, arg):
    return str((float(value) / float(arg)) * 100).replace(",", ".")


@register.inclusion_tag("core/navbar.html")
def navbar(navbar_links):
    return {"navbar_links": navbar_links}
