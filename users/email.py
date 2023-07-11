from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags

from config import settings


class Email:
    """
       A utility class for sending emails using Django's email framework.

       Attributes:
           from_email (str): The default email address to use as the sender.
    """
    from_email = settings.DEFAULT_FROM_EMAIL

    @staticmethod
    def _get_contents(html_file_name, **context):
        """
            usage: renders an HTML template and extracts the text content from html.

            Args:
                html_file_name (str): The name of the HTML template file to render.
                context (dict): Optional context data to be passed to the template.

            Returns:
                Tuple[str, str]: A tuple containing the plain text and HTML versions of
                the rendered template content.
        """

        html_content = render_to_string(html_file_name, context)
        text_content = strip_tags(html_content)
        return text_content, html_content

    @classmethod
    def send(cls, subject, to_email, text_content, html_content=None):
        """
            usage: Sends an email with the specified subject, text content, and HTML content
                    to the specified email address.
            Args:
                subject (str): The subject of the email.
                to_email (str): The email address to send the email to.
                text_content (str): The plain text content of the email.
                html_content (str) (optional): The HTML content of the email.
        """

        try:
            email = EmailMultiAlternatives(subject, text_content, cls.from_email, [to_email])
            if html_content:
                email.attach_alternative(html_content, "text/html")

            email.send(fail_silently=False)

        except Exception as e:
            # Handle any exceptions that occur during sending
            raise Exception(f'Failed to send email: {str(e)}')

    @classmethod
    def send_signup_confirmation(cls, user):
        """
            usage: Sends an email to the user's email address containing a TOTP.
            Args:
                user (User): The user object of the user to send the email to.

        """
        if not user.totp:
            raise ValueError("TOTP must be saved before sending the confirmation email")

        contents = cls._get_contents('users/signup_email_confirmation.html', user=user)
        cls.send('Confirm your email address', user.email, *contents)

    @classmethod
    def send_password_reset(cls, request, user, token):
        """
           usage: Sends an email to the user's email address containing a link to reset their password.

           Args:
               request (HttpRequest): The current HTTP request object.
               user (User): The user object for the user to send the email to.
               token (str): The token for the password reset link.

        """
        reset_url = request.build_absolute_uri(reverse('password_reset_confirm', args=[token]))
        contents = cls._get_contents('users/reset_password_link.html', user=user, reset_url=reset_url)
        cls.send('Password reset request', user.email, *contents)

    @classmethod
    def send_change_password(cls, user):
        """
            usage: Sends an email to user to notify the password change.
            Args:
                user (User): The user object of the user to send the email to.
        """

        message = f'Hi {user.username}, your password has been changed successfully.'
        cls.send('Password changed', user.email, message)

    @classmethod
    def send_change_email(cls, user, new_email):
        """
            usage: Sends an email to the user's email address containing a TOTP.
            Args:
                user (User): The user object for the user to send the email to.
                new_email (str): The new email address for the user.
        """
        if not user.totp:
            raise ValueError("TOTP must be saved before sending the confirmation email")

        contents = cls._get_contents('users/change_email_confirmation.html', user=user, new_email=new_email)
        cls.send("Email Change Confirmation", user.email, *contents)
