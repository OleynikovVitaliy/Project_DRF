# Пагинацию реализуйте в отдельном файле
# paginators.py
# . Можно реализовать один или несколько классов пагинатора. Укажите параметры
# page_size
# ,
# page_size_query_param
# ,
# max_page_size
#  для класса
# PageNumberPagination
# . Количество элементов на странице выберите самостоятельно. Интегрируйте пагинатор в контроллеры, используя параметр
# pagination_class

from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
