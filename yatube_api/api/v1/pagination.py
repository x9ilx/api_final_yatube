from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class ListOrOffsetPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        if 'offset' not in self.request.GET or 'limit' not in self.request.GET:
            return Response(data)
        return super().get_paginated_response(data)
