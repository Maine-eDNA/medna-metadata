from django import template
from django.conf import settings


register = template.Library()


def pop_and_get_app(apps, key, app_label):
    for index, app in enumerate(apps):
        if app[key] == app_label:
            obj = apps.pop(index)
            return obj
    return None


@register.filter
def sort_apps(apps):
    new_apps = []
    order = settings.APP_ORDER
    for app_label in order.keys():
        obj = pop_and_get_app(apps, 'app_label', app_label)
        new_apps.append(obj) if obj else None
    apps = new_apps + apps
    for app in apps:
        models = app.get('models')
        app_label = app.get('app_label')
        new_models = []
        order_models = settings.APP_ORDER.get(app_label, [])
        for model in order_models:
            obj = pop_and_get_app(models, 'object_name', model)
            new_models.append(obj) if obj else None
        models = new_models + models
        app['models'] = models
    return apps
