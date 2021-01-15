from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm, ContactForm
from django.shortcuts import redirect, render


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("authForm")  # where login is the "name" parameter in path()
    template_name = "reg.html"


def user_contact(request):

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            return redirect('/thank-you/')
        return render(request, 'contact.html', {'form': form})
    form = ContactForm()
    return render(request, 'contact.html', {form: form})
