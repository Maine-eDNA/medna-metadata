from rest_framework.permissions import (DjangoModelPermissions)
# https://medium.com/innoventes/django-protect-apis-using-djangomodelpermissions-cb1bf65c5b58
# https://www.django-rest-framework.org/api-guide/permissions/#djangomodelpermissions


class CustomDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self):
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
