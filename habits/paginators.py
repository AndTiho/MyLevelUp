from rest_framework.pagination import PageNumberPagination


class MyPaginator(PageNumberPagination):
    """Пагинатор для вывода списка привычек по 5 на страницу"""

    page_size = 5
    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = 100
