from django import template

register = template.Library()


@register.inclusion_tag("components/list_events.html")
def list_events(events, title):
    return {"events": events, "title": title}
