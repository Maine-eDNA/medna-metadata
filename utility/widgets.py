from django import forms
from django.utils.safestring import mark_safe
from django.template import loader
from django.template.loader import render_to_string


class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'django/custom_forms/widgets/clearable_file_input.html'

    def render(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


class CustomFileInput(forms.ClearableFileInput):
    template_name = 'django/custom_forms/widgets/file.html'

    def render(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)
