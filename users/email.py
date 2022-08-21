from django.template import context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings 
 

def send_verification_email(name, email, verify_link):
    context = {
        'name'  : name,
        'email' : email,
        'verify_link': verify_link
    }
    email_subject = 'Thank you for your registration'
    email_body = render_to_string('email_verification.txt', context)

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ]
    )
    return email.send(fail_silently=False)
