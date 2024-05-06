from django import template
from main.models import Post

register = template.Library()


@register.simple_tag()
def latest_news_pk():
    l_news_pk = Post.get_latest_news_pk()
    return l_news_pk

