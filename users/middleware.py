import requests
from django.http import HttpResponseRedirect
from django.urls import reverse
# https://docs.djangoproject.com/en/3.2/topics/http/middleware/


# https://stackoverflow.com/questions/51188439/handling-django-user-subscription-expiry-date
# https://stackoverflow.com/questions/12270928/best-way-to-extend-django-authentication-authorization
# https://stackoverflow.com/questions/57235057/how-to-make-user-permissions-that-expire-after-24-hours
class AccountExpiry:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_user = request.user
        response = self.get_response(request)
        expiry_path = reverse('rest-auth:user')

        if current_user.is_anonymous is False:
            if current_user.admin is False and current_user.staff is False:
                if request.path not in [expiry_path]:
                    if current_user.is_expired is True:
                        return HttpResponseRedirect(expiry_path)
        return response
