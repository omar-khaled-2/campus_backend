from rest_framework import pagination
from rest_framework.response import Response

class Pagination(pagination.PageNumberPagination):
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response({
            "total_pages":self.page.paginator.num_pages,
            'total': self.page.paginator.count,
            'results': data
        })