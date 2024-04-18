from django_filters import FilterSet
from django_filters.widgets import RangeWidget

from .models import Post
from django_filters import DateFromToRangeFilter


# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    post_time = DateFromToRangeFilter(field_name='post_time', label='Дата поста', widget=RangeWidget(attrs={'type':'date'}))

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            'post_headline': ['icontains'],
            'post_text': ['icontains'],
        }

