from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


@login_required
def author(request):
    return render(request, 'about/author.html')


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('train:train_list')
    template_name = 'users/signup.html'
