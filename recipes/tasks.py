import logging
from django.urls import reverse
from django.core.mail import send_mail
from users.models import User


# from foodgram import settings


def send_verification_email(user_id):
    try:
        user = User.objects.get(id=user_id)
        # Send verification email
        send_mail(
            subject='Регистрация на foodgram',
            message='Добрый день, Вы получили это письмо так как зарегистрировались на сайте foodgram:'
                    'http://localhost:8000%s' % reverse('index'),
            from_email='bolshakov.developer@gmail.com',
            recipient_list=[user.email],
            fail_silently=False,
        )
    except User.DoesNotExist:
        logging.warning(
            "Tried to send verification email to non-existing user "
            "'%s'" % user_id)
