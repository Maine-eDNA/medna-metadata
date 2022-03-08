from rest_framework.permissions import (DjangoModelPermissions)
# https://medium.com/innoventes/django-protect-apis-using-djangomodelpermissions-cb1bf65c5b58
# https://www.django-rest-framework.org/api-guide/permissions/#djangomodelpermissions


class CustomDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self):
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']

    def has_permission(self, request, view):
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        if getattr(view, '_ignore_model_permissions', False):
            return True

        # if request.user.is_expired then their expiration date has elapsed the current date and no longer
        # has permission to use the API
        if not request.user or (
           not request.user.is_authenticated and self.authenticated_users_only) or request.user.is_expired:
            return False

        queryset = self._queryset(view)
        perms = self.get_required_permissions(request.method, queryset.model)

        return request.user.has_perms(perms)
