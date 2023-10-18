"""Django tests module for user registration"""

from django.test import TestCase
from django.urls import reverse


class BaseTest(TestCase):
    """Test class used for setting up for tests"""

    def setUp(self):
        """Method used to set up all the data that will be used for the test"""

        self.register_url = reverse('register')
        self.user = {
            'email': 'test.email@gmail.com',
            'username': 'testuser',
            'password': 'sword.master2',
            'password2': 'sword.master2',
            'name': 'TestUser'
        }
        self.user_short_pass = {
            'email': 'test2.email@gmail.com',
            'username': 'testuser2',
            'password': 'pass',
            'password2': 'pass',
            'name': 'Tester'
        }
        self.user_different_pass = {
            'email': 'test3.email@gmail.com',
            'username': 'testuser3',
            'password': 'sword',
            'password2': 'mygreatsword',
            'name': 'TestUser'
        }
        self.user_with_invalid_email = {
            'email': 'test.email.com',
            'username': 'testuser4',
            'password': 'mygreatsword',
            'password2': 'mygreatsword',
            'name': 'TestUser'
        }

        return super().setUp()


class RegistrationTest(BaseTest):
    """Test class used for testing registration functionality"""

    def test_register_page_can_be_viewed(self):
        """Method used to test if the register page can be viewed through a GET request"""

        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication_app/register.html')

    def test_successful_user_registration(self):
        """Method used to test successful user registration"""

        response = self.client.post(self.register_url, self.user, format='text/html')
        # Test to see if there is redirect to the login page
        self.assertEqual(response.status_code, 302)

    def test_registration_with_short_pass(self):
        """Method used to test unsuccessful user registration with shorter passwords"""

        response = self.client.post(self.register_url, self.user_short_pass, format='text/html')
        self.assertEqual(response.status_code, 400, 'Your password must be more than 6 characters')

    def test_registration_with_different_pass(self):
        """Method used to test unsuccessful user registration with different passwords"""

        response = self.client.post(self.register_url, self.user_different_pass, format='text/html')
        self.assertEqual(response.status_code, 400, 'Your passwords MUST match')

    def test_registration_with_invalid_email(self):
        """Method used to test registration with invalid email"""

        response = self.client.post(self.register_url, self.user_with_invalid_email, format='text/html')  # pylint: disable=line-too-long
        self.assertEqual(response.status_code, 400, 'Please provide a valid email')

    def test_registration_with_taken_email(self):
        """Method used to test registration with already taken email"""

        self.client.post(self.register_url, self.user, format='text/html')
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 400, 'Provided email is already taken')

    def test_registration_with_taken_username(self):
        """Method used to test registration with already taken username"""

        self.client.post(self.register_url, self.user, format='text/html')
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 400, 'Username is taken')
