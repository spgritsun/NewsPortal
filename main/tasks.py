import datetime

from celery import shared_task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from NewsPortal.settings import SITE_URL, DEFAULT_FROM_EMAIL
from main.models import Post, Category


@shared_task
def send_notification(preview, pk, post_headline, subscribers_email_list, cat_name_list):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{SITE_URL}/posts/{pk}',
            'cat_name_list': cat_name_list,

        }
    )
    msg = EmailMultiAlternatives(
        subject=post_headline,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers_email_list,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_daily_posts():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(post_time__gte=last_week)  # Берем все посты за последнюю неделю
    categories = set(posts.values_list('categories__category_name', flat=True))  # Получаем все названия категорий
    # этих постов
    subscribers = set(
        Category.objects.filter(category_name__in=categories).values_list('subscribers__email', flat=True))  # Из
    # объектов категорий постов извлекаем список email подписчиков на эти категории

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
