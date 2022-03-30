from django import forms
from django.contrib.admin.helpers import ActionForm
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser
from .widgets import CustomSelect2Multiple
from .models import ContactUs, Project, Publication


# custom import from import_export/forms.py
def export_action_form_factory(formats):
    """
    Returns an ActionForm subclass containing a ChoiceField populated with
    the given formats.
    """
    class _ExportActionForm(ActionForm):
        """
        Action form with export format ChoiceField.
        """
        file_format = forms.ChoiceField(
            label=_('Format'), choices=formats, required=False)
    _ExportActionForm.__name__ = str('ExportActionForm')

    return _ExportActionForm


########################################
# FRONTEND FORMS                       #
########################################
class PublicationForm(forms.ModelForm):
    # https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html
    # https://simpleisbetterthancomplex.com/article/2017/08/19/how-to-render-django-form-manually.html
    publication_title = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )
    publication_url = forms.URLField(
        required=True,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    project_names = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Project.objects.all(),
        widget=CustomSelect2Multiple(
            attrs={
                'class': 'form-control',
            }
        )
    )
    publication_authors = forms.ModelMultipleChoiceField(
        required=False,
        queryset=CustomUser.objects.all(),
        widget=CustomSelect2Multiple(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Publication
        fields = ['publication_title', 'publication_url', 'project_names', 'publication_authors', ]


class ContactUsForm(forms.ModelForm):
    # https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html
    # https://simpleisbetterthancomplex.com/article/2017/08/19/how-to-render-django-form-manually.html
    full_name = forms.CharField(
        required=True,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }
        )
    )
    contact_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'example@mail.com'
            }
        )
    )
    contact_context = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Describe your problem in at least 250 characters',
                'id': 'message',
                'rows': 6,
            }
        )
    )

    class Meta:
        model = ContactUs
        fields = ['full_name', 'contact_email', 'contact_context', ]

    # def send_email(self):
    #     # send email using the self.cleaned_data dictionary
    #     pass


class ContactUsUpdateForm(forms.ModelForm):
    # https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html
    # https://simpleisbetterthancomplex.com/article/2017/08/19/how-to-render-django-form-manually.html
    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }
        )
    )
    contact_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }
        )
    )
    contact_context = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'id': 'message',
                'rows': 6,
            }
        )
    )

    replied_context = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 6,
            }
        )
    )

    replied_datetime = forms.DateTimeField(
        required=True,
        widget=CustomDateTimePicker(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }
        )
    )

    class Meta:
        model = ContactUs
        fields = ['full_name', 'contact_email', 'contact_context', 'replied_context', 'replied_datetime', ]

    # def send_email(self):
    #     # send email using the self.cleaned_data dictionary
    #     pass
