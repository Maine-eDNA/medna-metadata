# users/adapters.py
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    # https://stackoverflow.com/questions/17923692/turn-off-user-social-registration-in-django-allauth
    def is_open_for_signup(self, request):
        """
        Whether to allow sign ups.
        """
        allow_signups = super(
            CustomAccountAdapter, self).is_open_for_signup(request)
        # Override with setting, otherwise default to super.
        return getattr(settings, 'ACCOUNT_ALLOW_SIGNUPS', allow_signups)
