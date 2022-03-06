from django import forms


class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'forms/widgets/clearable_file_input.html'


class CustomFileInput(forms.ClearableFileInput):
    template_name = 'forms/widgets/file.html'
