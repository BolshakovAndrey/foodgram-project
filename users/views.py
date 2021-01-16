from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm
from django.contrib.auth import logout


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login")  # where login is the "name" parameter in path()
    template_name = "users/signup.html"

