# snippets adapted from templatetags/admin_list.py
from django import template

register = template.Library()


@register.filter
def split_email(value):
    return value.split('@')[0]