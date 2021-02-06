from django.core.mail import send_mail


def email_default():
    from django.conf import settings

    return settings.GLOBAL_SETTINGS["EMAIL_DEFAULT_ADDRESS"]


def send_message(mail_subject, message, email):
    send_mail(
        mail_subject,
        message,
        email_default(),
        [email],
        fail_silently=False,
    )
