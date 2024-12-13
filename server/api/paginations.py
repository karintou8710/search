import math

from rest_framework import pagination
from rest_framework.response import Response


class SizePagination(pagination.PageNumberPagination):
    """総ページ数を含めてレスポンスする
    """

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'size': self.get_num_page(self.page.paginator.count, self.page_size),
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })

    @staticmethod
    def get_num_page(count, page_size):
        """総ページ数を求める

        Args:
            count: int, 総データ数
            page_size: int, ページ当たりのデータ数

        Return:
            int, 総ページ数
        """
        return math.ceil(count / page_size)
