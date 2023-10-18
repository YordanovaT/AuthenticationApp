"""Django tests module for user login"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class BaseTest(TestCase):
    """Test class used for setting up for tests"""

    def setUp(self):
        """Method used to set up all the data that will be used for the test"""

        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.user = {
            'email': 'test.email@gmail.com',
            'username': 'usertest',
            'password': 'sword.master2',
            'password2': 'sword.master2',
            'name': 'TestUserLogin'
        }

        return super().setUp()


class TestLogIn(BaseTest):
    """Test class used for testing login functionality"""
    def test_access_to_the_login_page(self):
        """Method used to test if the login page can be accessed"""

        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication_app/login.html')

    def test_successful_login(self):
        """
        Method used to test successful login after the user is created,
        a confirmation email has been sent to him and the account
        has been successfully activated
        """

        # the user is created in the database
        self.client.post(self.register_url, self.user, format='text/html')  # pylint: disable=line-too-long
        user = User.objects.filter(email=self.user['email']).first()
        user.is_active = True
        user.save()

        # after the user is successfully activated, he's logged in
        response = self.client.post(self.login_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_login_with_unverified_email(self):
        """
        Method used to test unsuccessful login where the user's email is not verified
        """

        # the user is created in the database
        self.client.post(self.register_url, self.user, format='text/html')  # pylint: disable=line-too-long
        response = self.client.post(self.login_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 401)

    def test_login_with_no_pass(self):
        """
        Method used to test unsuccessful login where the user don't provide password during login
        """

        # the user is created in the database
        self.client.post(self.register_url, self.user, format='text/html')  # pylint: disable=line-too-long
        user = User.objects.filter(email=self.user['email']).first()
        user.is_active = True
        user.save()

        self.user['password'] = ''
        response = self.client.post(self.login_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 401, 'Password is required for user login')

    def test_login_with_no_username(self):
        """
        Method used to test unsuccessful login where the user don't provide username during login
        """

        # the user is created in the database
        self.client.post(self.register_url, self.user, format='text/html')  # pylint: disable=line-too-long
        user = User.objects.filter(email=self.user['email']).first()
        user.is_active = True
        user.save()

        self.user['username'] = ''
        response = self.client.post(self.login_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 401, 'Username is required for user login')
