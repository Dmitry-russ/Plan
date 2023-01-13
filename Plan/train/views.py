from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .models import Image, Cases, Train, User
from .utils import page_control


PAGE_LIST = 30

def train_list(request):
    cases = Train.objects.select_related('cases')
    page_obj = page_control(request, cases, PAGE_LIST)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'train/train_list.html', context)

def cases_list(request, id):
    train = get_object_or_404(Train, id=id)
    cases = train.cases
    page_obj = page_control(request, cases, PAGE_LIST)
    context = {
        'page_obj': page_obj,
        'train': train,
    }
    return render(request, 'train/cases_list.html', context)

def case_detail(request, id):
    case = get_object_or_404(Cases, id=id)
    context = {
        'case': case,
    }
    return render(request, 'train/case_detail.html', context)