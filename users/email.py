from django.core.mail import EmailMultiAlternatives
from django.urls import reverse

from config import settings


class SendEmail:
    @classmethod
    def send(cls, subject, from_email, recipient_list, message):
        try:

            # Create an email message with both plain text and HTML content
            email = EmailMultiAlternatives(
                subject=subject,
                body=message,
                from_email=from_email,
                to=recipient_list
            )

            # Send the email
            email.send(fail_silently=False)

        except Exception as e:

            # Handle any exceptions that occur during sending
            raise Exception(f'Failed to send email: {str(e)}')

    @classmethod
    def send_signup_confirmation(cls, request, user, token):

        # Generate the URL for the confirmation link
        confirm_url = request.build_absolute_uri(reverse('confirm_signup', args=[str(token[0])]))

        message = f'Hi {user.email}, please click the link below to confirm your account:\n{confirm_url}'
        cls.send(
            subject='Confirm your email address',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            message=message,
        )

    @classmethod
    def send_password_reset(cls, request, user, token):

        # Generate the URL for the password reset link
        password_reset_url = request.build_absolute_uri(reverse('password_reset_confirm', args=[str(token.key)]))

        message = f'Hi {user.username},' \
                  f'\n\nYou recently requested to reset your password for your account at {password_reset_url}.'
        cls.send(
            subject='Password reset request',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            message=message,
        )

    @classmethod
    def send_change_password(cls, user):
        message = f'Hi {user.username}, your password has been changed successfully.'
        cls.send(
            subject='Password changed',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            message=message,
        )

    @classmethod
    def send_change_email(cls, new_email):
        cls.send(
            subject="Email Change Confirmation",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[new_email],
            message=f"Your email has been changed to {new_email}.",
        )
