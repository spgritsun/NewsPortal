from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, NewsDetail, PostList1, PostList2, PostCreate, PostUpdate, PostDelete

urlpatterns = [
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('news/', PostList.as_view(), name='news_list'),
   path('articles/', PostList.as_view(), name='articles_list'),
   path('news/search/', PostList1.as_view()),
   path('articles/search/', PostList1.as_view()),
   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('articles/create/', PostCreate.as_view(), name='articles_create'),
   path('news/<int:pk>/', NewsDetail.as_view(), name='post_detail'),
   path('articles/<int:pk>/', NewsDetail.as_view(), name='post_detail'),
   path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='product_delete'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='product_delete'),
   path('posts/<int:pk>/', NewsDetail.as_view(), name='post_detail'),
   path('posts/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('posts/<int:pk>/delete/', PostDelete.as_view(), name='product_delete'),
   path('posts/', PostList2.as_view(), name='post_list'),
]