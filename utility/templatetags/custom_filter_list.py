# snippets adapted from templatetags/admin_list.py
from django import template
from django.utils.html import escape
from django.core.exceptions import ImproperlyConfigured
from django.template import Node, TemplateSyntaxError
from django.utils.http import urlencode

context_processor_error_msg = (
    "Tag {%% %s %%} requires django.template.context_processors.request to be "
    "in the template configuration in "
    "settings.TEMPLATES[]OPTIONS.context_processors) in order for the included "
    "template tags to function correctly."
)
register = template.Library()


@register.inclusion_tag('users/actions.html', takes_context=True)
def custom_filter_actions(context):
    """
    Track the number of times the action field has been rendered on the page,
    so we know which value to use.
    """
    context['action_index'] = context.get('action_index', -1) + 1
    return context


@register.filter
def split_email(value):
    return value.split('@')[0]


class QuerystringNode(Node):
    def __init__(self, updates, removals, asvar=None):
        super().__init__()
        self.updates = updates
        self.removals = removals
        self.asvar = asvar

    def render(self, context):
        if "request" not in context:
            raise ImproperlyConfigured(context_processor_error_msg % "querystring")

        params = dict(context["request"].GET)
        for key, value in self.updates.items():
            if isinstance(key, str):
                params[key] = value
                continue
            key = key.resolve(context)
            value = value.resolve(context)
            if key not in ("", None):
                params[key] = value
        for removal in self.removals:
            params.pop(removal.resolve(context), None)

        value = escape("?" + urlencode(params, doseq=True))

        if self.asvar:
            context[str(self.asvar)] = value
            return ""
        else:
            return value

@register.simple_tag(takes_context=True)
def custom_export_url(context, export_trigger_param=None):
    """
    Returns an export URL for the given file `export_format`, preserving current
    query string parameters.

    Example for a page requested with querystring ``?q=blue``::

        {% custom_export_url %}

    It will return::

        ?q=blue&amp;_export=csv
    """

    if export_trigger_param is None and "view" in context:
        export_trigger_param = getattr(context["view"], "export_trigger_param", None)

    export_trigger_param = export_trigger_param or "_export"
    export_format = ""

    return QuerystringNode(updates={export_trigger_param: export_format}, removals=[]).render(
        context
    )

