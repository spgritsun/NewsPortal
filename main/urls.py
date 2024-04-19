from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, NewsDetail, PostList1, PostList2, PostCreate, PostUpdate, PostDelete

urlpatterns = [
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('news/', PostList.as_view()),
   path('news/search/', PostList1.as_view()),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('posts/', PostList2.as_view(), name='post_list'),
   path('news/<int:pk>/', NewsDetail.as_view(), name='post_detail'),
   path('news/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='product_delete'),
   path('posts/<int:pk>/', NewsDetail.as_view(), name='post_detail'),
   path('posts/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('posts/<int:pk>/delete/', PostDelete.as_view(), name='product_delete'),
]