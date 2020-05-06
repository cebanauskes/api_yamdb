from rest_framework import pagination
from rest_framework.response import Response


class GenrePagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {

            },
            'count': self.page.paginator.count,
            'response': data,
        })


class CategoryPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {

            },
            'count': self.page.paginator.count,
            'response': data,
        })
