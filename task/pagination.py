from rest_framework.pagination import PageNumberPagination


class TaskPagination(PageNumberPagination):
    page_size = 2#На одну страницу 10 объектов
    page_size_query_param ='page_size'#Если в параметрах запроса передать page_size какое то число он поделит объекты на страницы по этому числу
    max_page_size = 15#Ограничение page_size

#До параметра обязательно вопросительный знак