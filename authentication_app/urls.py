from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
urlpatterns=[
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path('', login_required(views.HomeView.as_view()), name='home'),
    path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(), name='activate'),
    path('set-new-pass/<uidb64>/<token>', views.SetNewPass.as_view(), name='set-new-pass'),
    path('reset-password/', views.RessetPasswordRequest.as_view(), name='reset-password')
]
