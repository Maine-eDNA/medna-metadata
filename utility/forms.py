from django import forms
from .models import ContactUs


# FRONTEND
class ContactUsForm(forms.ModelForm):
    # https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html

    class Meta:
        model = ContactUs
        fields = ('full_name', 'contact_email', 'contact_context', )
