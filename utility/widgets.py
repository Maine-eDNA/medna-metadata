from django import forms
from django.urls import reverse_lazy
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from django.utils.translation import gettext as _
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
        js = ('assets/js/plugins/jquery-3.4.1.min.js',
              'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js',
              'assets/js/custom-select2.js', )

    template_name = 'custom_forms/widgets/select2.html'
    option_template_name = 'custom_forms/widgets/select2_option.html'

    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'class': 'js-example-basic-single form-control'}
        super(CustomSelect2, self).__init__(*args, **kwargs)


class CustomSelect2Multiple(forms.SelectMultiple):
    class Media:
        css = {'all': ('https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css', )}
        js = ('assets/js/plugins/jquery-3.4.1.min.js',
              'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js',
              'assets/js/custom-select2.js', )

    template_name = 'custom_forms/widgets/select2.html'
    option_template_name = 'custom_forms/widgets/select2_option.html'

    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'class': 'js-example-basic-multiple form-control'}
        super(CustomSelect2Multiple, self).__init__(*args, **kwargs)


class CustomAdminDateWidget(AdminDateWidget):
    # https://stackoverflow.com/questions/61077802/how-to-use-a-datepicker-in-a-modelform-in-django/69108038#69108038
    class Media:
        css = {'all': ('admin/css/widgets.css', )}
        js = ['admin/js/core.js',
              reverse_lazy('jsi18n'),
              'admin/js/calendar.js',
              'admin/js/admin/DateTimeShortcuts.js', ]

    template_name = 'custom_forms/widgets/date.html'

    def __init__(self, attrs=None, format=None):
        attrs = {'class': 'vDateField form-control', 'size': '10', **(attrs or {})}
        super().__init__(attrs=attrs, format=format)


class CustomAdminTimeWidget(AdminTimeWidget):
    # https://stackoverflow.com/questions/61077802/how-to-use-a-datepicker-in-a-modelform-in-django/69108038#69108038
    class Media:
        css = {'all': ('admin/css/widgets.css', )}
        js = ['admin/js/core.js',
              reverse_lazy('jsi18n'),
              'admin/js/calendar.js',
              'admin/js/admin/DateTimeShortcuts.js', ]

    template_name = 'custom_forms/widgets/time.html'

    def __init__(self, attrs=None, format=None):
        attrs = {'class': 'vTimeField form-control', 'size': '8', **(attrs or {})}
        super().__init__(attrs=attrs, format=format)


class CustomAdminSplitDateTime(AdminSplitDateTime):
    """
    A SplitDateTime Widget that has some admin-specific styling.
    """
    template_name = 'custom_forms/admin_widgets/split_datetime.html'

    def __init__(self, attrs=None):
        widgets = [CustomAdminDateWidget, CustomAdminTimeWidget]
        # Note that we're calling MultiWidget, not SplitDateTimeWidget, because
        # we want to define widgets.
        forms.MultiWidget.__init__(self, widgets, attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['date_label'] = _('Date:')
        context['time_label'] = _('Time:')
        return context
