from rest_framework.pagination import PageNumberPagination


class IdeaPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    page_size = 50
    max_page_size = 50


class CommentPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    page_size = 20
    max_page_size = 50


class TagPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    page_size = 20
    max_page_size = 50
