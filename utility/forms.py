from django import forms
from .models import ContactUs


# FRONTEND
class ContactUsForm(forms.Form):
    # https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html
    # https://simpleisbetterthancomplex.com/article/2017/08/19/how-to-render-django-form-manually.html
    full_name = forms.CharField(
        required=True,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'style': 'form-control',
                'placeholder': 'Full Name',
                'id': None,
            }
        )
    )
    full_name.widget.attrs.pop('id', None)
    contact_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'style': 'form-control',
                'placeholder': 'Full Name'
            }
        )
    )
    contact_context = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'style': 'form-control',
                'placeholder': 'Describe your problem in at least 250 characters',
                'id': 'message',
                'rows': 6,
            }
        )
    )

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass
