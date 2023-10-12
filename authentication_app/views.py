from django.shortcuts import render, redirect
from django.views.generic import View
from validate_email import validate_email
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.


class RegistrationView(View):
    """
    Class view used for the registration functionality
    """

    def getpage(self, request):

        return render(request, 'authentication_app/register.html')

    def create_registration(self, request):
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
            return render(request, 'authentication_app/register.html', context)

        # If there are no errors, then we create the user
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.first_name = full_name
        user.last_name = full_name
        user.is_active=False

        user.save()
        messages.add_message(request, messages.SUCCESS, 'Account successfully created! ')
        return redirect('login')


class LoginView(View):
    """Class used for user login"""

    def getpage(self, request):

        return render(request, 'authentication_app/login.html')
