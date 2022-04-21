from django import template

register = template.Library()


@register.filter(name='field_type')
def field_type(ob):
    return ob.__class__.__name__
