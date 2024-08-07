
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator


def send_confirmation_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    confirm_url = f"{'localhost/registration/confirm'}/{uid}/{token}/"

    subject = 'Confirm your registration'
    message = f'Please click the following link to confirm your registration: {confirm_url}'
    html_message = render_to_string('registration/registration_confirmation_email.html', {'confirm_url': confirm_url})

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=html_message)
