from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


# https://www.django-rest-framework.org/api-guide/pagination/#example
class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })
