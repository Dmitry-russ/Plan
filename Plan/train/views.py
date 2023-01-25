from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CasesForm, NewTrainForm, NewMaiForm
from .models import Cases, Train, Maintenance
from .utils import page_control

PAGE_LIST = 30


@login_required
def train_list(request):
    cases = Train.objects.all()
    page_obj = page_control(request, cases, PAGE_LIST)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'trains/train_list.html', context)


@login_required
def cases_list(request, train_id):
    train = get_object_or_404(Train, id=train_id)
    cases = Cases.objects.filter(train=train)
    page_obj = page_control(request, cases, PAGE_LIST)
    context = {
        'page_obj': page_obj,
        'train': train,
    }
    return render(request, 'trains/cases_list.html', context)


@login_required
def case_detail(request, case_id):
    case = Cases.objects.select_related().get(id=case_id)
    form = CasesForm(
        request.POST or None,
        files=request.FILES or None,
        instance=case)
    if form.is_valid():
        case.save()
        form = CasesForm(
            request.POST or None,
            files=request.FILES or None,
            instance=case)

    context = {'form': form,
               'case': case,
               'is_edit': True, }
    return render(request, 'trains/case_detail.html', context)


@login_required
def case_create(request, train_id):
    form = CasesForm(request.POST or None, files=request.FILES or None)
    train = get_object_or_404(Train, id=train_id)
    context = {'form': form,
               'train': train}
    if not form.is_valid():
        return render(request, 'trains/case_create.html', context)
    case = form.save(commit=False)
    case.author = request.user
    case.train = train
    case.save()
    return redirect('train:cases_list', train.id)


@login_required
def train_create(request):
    form = NewTrainForm(request.POST or None, files=request.FILES or None)
    context = {'form': form}
    if not form.is_valid():
        return render(request, 'trains/train_create.html', context)
    train = form.save(commit=False)
    train.author = request.user
    train.save()
    return redirect('train:train_list')


@login_required
def case_delete(request, case_id, train_id):
    case = Cases.objects.filter(id=case_id)
    if case.exists():
        case.delete()
    return redirect('train:cases_list', train_id)


@login_required
def mai_list(request, train_id):
    train = get_object_or_404(Train, id=train_id)
    mai = Maintenance.objects.filter(train=train)
    page_obj = page_control(request, mai, PAGE_LIST)
    context = {
        'page_obj': page_obj,
        'train': train,
    }
    return render(request, 'trains/mai_list.html', context)


@login_required
def mai_create(request, train_id):
    form = NewMaiForm(request.POST or None, files=request.FILES or None)
    train = get_object_or_404(Train, id=train_id)
    context = {'form': form,
               'train': train,
               }
    if not form.is_valid():
        return render(request, 'trains/mai_create.html', context)
    mai = form.save(commit=False)
    mai.author = request.user
    mai.train = train
    mai.save()
    return redirect('train:mai_list', train_id)
