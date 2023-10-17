from django.shortcuts import render, redirect
from django.views.generic import View
from validate_email import validate_email
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError

from django.core.mail import EmailMessage
from django.conf import settings

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# Create your views here.


class RegistrationView(View):
    """
    Class view used for the registration functionality
    """

    def get(self, request):
        """ Method used to GET the register page """

        return render(request, 'authentication_app/register.html')

    def post(self, request):
        """Method used for registration"""

        context = {'has_error': False}
        data = request.POST
        context['data'] = data

        email = request.POST.get('email')
        username = request.POST.get('username')
        full_name = request.POST.get('name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not validate_email(email):
            messages.add_message(request, messages.ERROR, 'Please provide a valid email')
            context['has_error'] = True

        try:
            if User.objects.get(email=email):
                messages.add_message(request, messages.ERROR, 'Provided email is already taken')
                context['has_error'] = True
        except Exception as identifier:
            pass

        try:
            if User.objects.get(username=username):
                messages.add_message(request, messages.ERROR, 'Username is taken')
                context['has_error'] = True
        except Exception as identifier:
            pass

        if len(password) < 6:
            messages.add_message(request, messages.ERROR, 'Your password must be more than 6 characters')
            context['has_error'] = True

        if password2 != password:
            messages.add_message(request, messages.ERROR, 'Your passwords MUST match')
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'authentication_app/register.html', context, status=400)

        # If there are no errors, then we create the user
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.first_name = full_name
        user.last_name = full_name
        user.is_active = False

        user.save()

        # Creating link

        current_site = get_current_site(request)  # Get the site's domain
        email_subject = 'Activate your account'
        message = render_to_string('authentication_app/activate.html',
                                   {'user': user, 'domain': current_site.domain,
                                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                    'token': token_generator.make_token(user)  # Can use it also for account activation
                                    })  # encode user id as bytes

        send_email = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [email])

        send_email.send()

        messages.add_message(request, messages.SUCCESS, 'Account successfully created! '
                                                        'A confirmation email has been sent to you.')
        return redirect('login')


class LoginView(View):
    """Class used for user login"""

    def get(self, request):
        """ Method used to GET the login page """

        return render(request, 'authentication_app/login.html')

    def post(self, request):
        """ Method used for user login """

        context = {'has_error': False,
                   'data': request.POST
                   }

        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == '':
            messages.add_message(request, messages.ERROR, 'Username is required for user login')
            context['has_error'] = True

        if password == '':
            messages.add_message(request, messages.ERROR, 'Password is required for user login')
            context['has_error'] = True

        user = authenticate(request, username=username, password=password)

        if not user and not context['has_error']:  # Checking if authentication method has failed
            messages.add_message(request, messages.ERROR, 'Invalid login. Try to login again')
            context['has_error'] = True
        if context['has_error']:
            return render(request, 'authentication_app/login.html', status=401, context=context)

        # If there are no errors:
        login(request, user)

        return redirect('home')


class ActivateAccountView(View):

    def get(self, request, uidb64, token):
        """Check if the parameters are correct in order to successfully verify account through link"""

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
        except Exception as identifier:
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            messages.add_message(request, messages.SUCCESS, ' You successfully activated your account.')

            return redirect('login')
        return render(request, 'authentication_app/activation_failed.html', status=401)


class HomeView(View):

    def get(self, request):
        """ Method used to GET the home page """
        return render(request, 'home.html')


class LogOutView(View):
    def post(self, request):
        logout(request)
        messages.add_message(request, messages.SUCCESS, ' You successfully logged out.')
        return redirect('login')


class RessetPasswordRequest(View):

    def get(self, request):
        """ Method used to GET the home page """

        return render(request, 'authentication_app/request_reset_email.html')

    def post(self, request):
        """ Method used send email for password resetting """

        context = {'has_error': False}
        email = request.POST['email']

        # check to see if there is a user with the provided email

        if not validate_email(email):
            messages.add_message(request, messages.ERROR, 'Please, enter valid email.')
            context['has_error'] = True

            return render(request, 'authentication_app/request_reset_email.html')

        # check to see if there is a user with the provided email
        user = User.objects.filter(email=email)

        if user.exists():  # send email only to users who have an account
            # Creating link

            current_site = get_current_site(request)  # Get the site's domain
            email_subject = 'Resset your password'
            message = render_to_string('authentication_app/reset_pass.html',
                                       {'domain': current_site.domain,
                                        'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                                        'token': PasswordResetTokenGenerator().make_token(user[0])
                                        # Can use it also for account activation
                                        })  # encode user id as bytes

            send_email = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email])

            send_email.send()

            messages.add_message(request, messages.SUCCESS,
                                 'We have sent an email with instructions on how to reset you password.')
        if context['has_error']:
            return render(request, 'authentication_app/request_reset_email.html', status=401, context=context)

        return render(request, 'authentication_app/request_reset_email.html')


class SetNewPass(View):
    def get(self, request, uidb64, token):
        """ Method used to GET the reset password page """

        context = {'uidb64': uidb64,
                   'token': token
                   }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))

            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, 'Password reset link is has expired. Please, request a new one.')

                return render(request, 'authentication_app/request_reset_email.html')

        except DjangoUnicodeDecodeError as identifier:
            messages.add_message(request, messages.ERROR, 'Invalid link')
            return render(request, 'authentication_app/request_reset_email.html')

        return render(request, 'authentication_app/set_new_password.html', context)

    def post(self, request, uidb64, token):
        """ Method used to reset user's password """

        context = {'uidb64': uidb64,
                   'token': token,
                   'has_error': False
                   }
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if len(password) < 6:
            messages.add_message(request, messages.ERROR, 'Your password must be more than 6 characters')
            context['has_error'] = True

        if password2 != password:
            messages.add_message(request, messages.ERROR, 'Your passwords MUST match')
            context['has_error'] = True

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))

            user=User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()

            messages.add_message(request, messages.SUCCESS,
                                 'You have successfully reset your password! You can login with the new password.')

            return redirect('login')

        except DjangoUnicodeDecodeError as identifier:
            messages.add_message(request, messages.ERROR, 'Something went wrong')
            return render(request, 'authentication_app/set_new_password.html', context)
