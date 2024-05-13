from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from NewsPortal.settings import SITE_URL, DEFAULT_FROM_EMAIL
from main.models import PostCategory


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

        send_notification(instance.preview(), instance.pk, instance.post_headline, subscribers_email_list,
                          cat_name_list)
