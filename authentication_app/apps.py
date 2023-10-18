"""Django apps module"""

from django.apps import AppConfig


class AuthenticationAppConfig(AppConfig):
    """Class used to configure the django application"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication_app'
