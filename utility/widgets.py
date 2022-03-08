from django import forms
from django.utils.safestring import mark_safe
from django.template import loader
# from django.template.loader import render_to_string


class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'custom_forms/widgets/clearable_file_input.html'


class CustomFileInput(forms.ClearableFileInput):
    template_name = 'custom_forms/widgets/file.html'
