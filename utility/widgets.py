import copy
import django
from django import forms
from django.contrib.admin.views.main import IS_POPUP_VAR
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django import forms
from django.urls import reverse_lazy
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime, RelatedFieldWidgetWrapper
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


class WidgetWrapperMixin(object):
    @property
    def is_hidden(self):
        return self.widget.is_hidden

    @property
    def media(self):
        return self.widget.media

    def build_attrs(self, extra_attrs=None, **kwargs):
        "Helper function for building an attribute dictionary."
        self.attrs = self.widget.build_attrs(extra_attrs=None, **kwargs)
        return self.attrs

    def value_from_datadict(self, data, files, name):
        return self.widget.value_from_datadict(data, files, name)

    def id_for_label(self, id_):
        return self.widget.id_for_label(id_)


class BaseRelatedWidgetWrapper(WidgetWrapperMixin, forms.Widget):
    """
    Basis for the specialised wrappers below.
    Don't call this directly, use some of the subclasses instead.
    """

    #: The template that is used to render the add-another button.
    #: Overwrite this to customize the rendering.
    template = 'custom_forms/admin_widgets/related_widget_wrapper.html'

    class Media:
        css = {'all': ('admin/css/widgets.css', )}
        js = (reverse_lazy('jsi18n'),
              'assets/js/plugins/jquery-3.4.1.min.js',
              'assets/js/django/admin/RelatedObjectLookups.js',
              )

    def __init__(self, widget, add_related_url,
                 edit_related_url, add_icon=None, edit_icon=None):
        if isinstance(widget, type):
            widget = widget()
        if add_icon is None:
            add_icon = 'admin/img/icon-addlink.svg'
        if edit_icon is None:
            edit_icon = 'admin/img/icon-changelink.svg'
        self.widget = widget
        self.attrs = widget.attrs
        self.add_related_url = add_related_url
        self.add_icon = add_icon
        self.edit_related_url = edit_related_url
        self.edit_icon = edit_icon

    def __deepcopy__(self, memo):
        obj = super(BaseRelatedWidgetWrapper, self).__deepcopy__(memo)
        obj.widget = copy.deepcopy(self.widget)
        return obj

    def render(self, name, value, *args, **kwargs):
        self.widget.choices = self.choices

        url_params = "%s=%s" % (IS_POPUP_VAR, 1)
        context = {
            'widget': self.widget.render(name, value, *args, **kwargs),
            'name': name,
            'url_params': url_params,
            'add_related_url': self.add_related_url,
            'add_icon': self.add_icon,
            'edit_related_url': self.edit_related_url,
            'edit_icon': self.edit_icon,
        }
        return mark_safe(render_to_string(self.template, context))


class AddAnotherWidgetWrapper(BaseRelatedWidgetWrapper):
    """Widget wrapper that adds an add-another button next to the original widget."""

    def __init__(self, widget, add_related_url, add_icon=None):
        super(AddAnotherWidgetWrapper, self).__init__(
            widget, add_related_url, None, add_icon, None
        )


class EditSelectedWidgetWrapper(BaseRelatedWidgetWrapper):
    """Widget wrapper that adds an edit-related button next to the original widget."""

    def __init__(self, widget, edit_related_url, edit_icon=None):
        super(EditSelectedWidgetWrapper, self).__init__(
            widget, None, edit_related_url, None, edit_icon
        )


class AddAnotherEditSelectedWidgetWrapper(BaseRelatedWidgetWrapper):
    """Widget wrapper that adds both add-another and edit-related button
    next to the original widget.
    """