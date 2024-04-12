from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, NewsDetail

urlpatterns = [
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostList.as_view()),
   path('<int:pk>', NewsDetail.as_view()),
]