from foodgram.settings import RESULTS_PER_PAGE
from rest_framework.pagination import PageNumberPagination


class RecipePagination(PageNumberPagination):
    """Pagination for the project."""

    page_size = RESULTS_PER_PAGE
    page_size_query_param = "limit"
