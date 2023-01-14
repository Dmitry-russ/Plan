from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .models import Image, Cases, Train, User
from .utils import page_control


PAGE_LIST = 30

def train_list(request):
    cases = Train.objects.all()
    page_obj = page_control(request, cases, PAGE_LIST)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'trains/train_list.html', context)

def cases_list(request, train_id):
    train = get_object_or_404(Train, id=train_id)
    cases = Cases.objects.filter(train=train)
    # cases = train.cases.all
    page_obj = page_control(request, cases, PAGE_LIST)
    context = {
        'page_obj': page_obj,
        'train': train,
    }
    return render(request, 'trains/cases_list.html', context)

def case_detail(request, case_id):
    case = get_object_or_404(Cases, id=case_id)
    context = {
        'case': case,
    }
    return render(request, 'trains/case_detail.html', context)

