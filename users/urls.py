from django.urls import path
# from django.contrib.auth.views import PasswordResetView, PasswordChangeDoneView

from . import views

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="signup"),
    # path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    # path('password-change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
]
