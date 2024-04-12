from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, NewsDetail, PostList1

urlpatterns = [
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('news/', PostList.as_view()),
   path('posts/', PostList1.as_view()),
   path('news/<int:pk>', NewsDetail.as_view()),
]