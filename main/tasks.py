from celery import shared_task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPortal.settings import SITE_URL, DEFAULT_FROM_EMAIL


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
