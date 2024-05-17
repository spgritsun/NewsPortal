from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from NewsPortal.settings import SITE_URL, DEFAULT_FROM_EMAIL
from main.models import PostCategory
from main.tasks import send_notification


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.categories.all()
        subscribers = []
        cat_name_list = []
        # categories_list = []
        for category in categories:
            subscribers += category.subscribers.all()
            cat_name_list.append(category.category_name)

        subscribers_email_list = [subscriber.email for subscriber in subscribers if subscriber.email]

        send_notification.delay(instance.preview(), instance.pk, instance.post_headline, subscribers_email_list,
                                cat_name_list)
