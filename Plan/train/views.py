from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from ..Plan.models import Image, Cases, Train, User
from .utils import page_control


PAGE_LIST = 10

def index(request):
    cases = Cases.objects.select_related('train')
    page_obj = page_control(request, cases, PAGE_LIST)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)