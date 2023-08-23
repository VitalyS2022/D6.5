from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import PostCategory


def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_emails.html',
        {'text': preview,
        'link': f'{settings.SITE_URL}/news/{pk}'
         })

    message = EmailMultiAlternatives(subject=title, body='', from_email=settings.DEFAULT_FROM_EMAIL, to=subscribers)

    message.attach_alternative(html_content, 'text/html')
    message.send()

@receiver(m2m_changed, sender=PostCategory)
def notification(sender, instance, **kwargs):
    if kwargs["action"] == 'post_add':
        categories = instance.category.all()
        subscribers = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers)




