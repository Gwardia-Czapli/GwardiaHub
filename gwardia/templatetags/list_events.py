from django import template

register = template.Library()


@register.inclusion_tag("gwardia/list_events.html")
def list_events(events, title):
    return {"events": events, "title": title}
