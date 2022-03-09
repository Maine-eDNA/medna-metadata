from django import forms
from django.utils.safestring import mark_safe
from django.template import loader
# from django.template.loader import render_to_string


class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'custom_forms/widgets/clearable_file_input.html'


class CustomFileInput(forms.FileInput):
    template_name = 'custom_forms/widgets/file.html'


class CustomRadioSelect(forms.RadioSelect):
    template_name = 'custom_forms/widgets/radio.html'
    option_template_name = 'custom_forms/widgets/radio_option.html'


class CustomSelect2(forms.Select):
    class Media:
        css = {'all': ('https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css', )}
        js = ('https://code.jquery.com/jquery-3.4.1.min.js',
              'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js',
              'assets/js/custom-select2.js', )

    template_name = 'custom_forms/widgets/select2.html'
    option_template_name = 'custom_forms/widgets/select2_option.html'

    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'class': 'js-example-basic-single'}
        super(CustomSelect2, self).__init__(*args, **kwargs)


class CustomSelect2Multiple(forms.SelectMultiple):
    class Media:
        css = {'all': ('https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css', )}
        js = ('https://code.jquery.com/jquery-3.4.1.min.js',
              'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js',
              'assets/js/custom-select2.js', )

    template_name = 'custom_forms/widgets/select2.html'
    option_template_name = 'custom_forms/widgets/select2_option.html'

    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'class': 'js-example-basic-multiple'}
        super(CustomSelect2Multiple, self).__init__(*args, **kwargs)


