"""Django utils module"""

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class TokenGenerator(PasswordResetTokenGenerator):
    """
        Class that is used for activating user's account and checking if he has token
        in order to use other functionalities of the application
    """
    def _make_hash_value(self, user, timestamp):
        """
        Overriding this method in order to
        have one-time-click emails for account confirmation.
        """

        return six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_active)


token_generator=TokenGenerator()
