from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'forms/widgets/clearable_file_input.html'

    def render(self):
        return mark_safe(render_to_string(self.template_name))


class CustomFileInput(forms.ClearableFileInput):
    template_name = 'forms/widgets/file.html'

    def render(self):
        return mark_safe(render_to_string(self.template_name))
