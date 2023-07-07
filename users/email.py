from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags

from config import settings


class Email:
    from_email = settings.DEFAULT_FROM_EMAIL

    @classmethod
    def send(cls, subject, text_content, html_content, to_email, ):
        # try:
        email = EmailMultiAlternatives(subject, text_content, cls.from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        # Send the email
        email.send(fail_silently=False)

        # except Exception as e:
        #
        #     # Handle any exceptions that occur during sending
        #     raise Exception(f'Failed to send email: {str(e)}')

    @classmethod
    def send_signup_confirmation(cls, user):
        html_content = render_to_string('users/signup_email_confirmation.html', {'user': user})
        text_content = strip_tags(html_content)
        cls.send('Confirm your email address', text_content, html_content, user.email)

    @classmethod
    def send_password_reset(cls, request, user, token):
        # Generate the URL for the password reset link
        reset_url = request.build_absolute_uri(reverse('password_reset_confirm', args=[str(token.key)]))
        html_content = render_to_string('users/reset_password_link.html', {'user': user, 'reset_url': reset_url})
        text_content = strip_tags(html_content)
        cls.send('Password reset request', text_content, html_content, user.email)

    # @classmethod
    # def send_change_password(cls, user):
    #     message = f'Hi {user.username}, your password has been changed successfully.'
    #     cls.send(
    #         subject='Password changed',
    #         from_email=settings.DEFAULT_FROM_EMAIL,
    #         recipient_list=[user.email],
    #         message=message,
    #     )

    @classmethod
    def send_change_email(cls, user, new_email):
        html_content = render_to_string('users/change_email_confirmation.html', {'user': user, 'new_email': new_email})
        text_content = strip_tags(html_content)
        cls.send("Email Change Confirmation", text_content, html_content, user.email)
