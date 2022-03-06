from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'django/forms/widgets/clearable_file_input.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget'].update({
            'template_name': self.template_name,
        })
        return context


class CustomFileInput(forms.ClearableFileInput):
    template_name = 'django/forms/widgets/file.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget'].update({
            'template_name': self.template_name,
        })
        return context
