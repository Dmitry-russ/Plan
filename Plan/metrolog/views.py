from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import NewMetrolog
from .models import Measurement
from django.shortcuts import get_object_or_404, redirect, render


def index(request):
    return HttpResponse("В стадии разработки.")


@login_required
def metrolog_create(request):
    """Создание инструмента СИ."""

    form = NewMetrolog(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(
            request,
            'metrolog/metrolog_create.html',
            {'form': form, 'is_edit': False, }
        )
    metrolog = form.save(commit=False)
    metrolog.author = request.user
    metrolog.save()
    return redirect('train:train_list')

@login_required
def metrolog_detail(request, metrolog_id):
    """Изменение инструмента СИ."""

    metrolog = get_object_or_404(Measurement, id=metrolog_id)
    form = NewMetrolog(
        request.POST or None,
        files=request.FILES or None,
        instance=metrolog)
    if form.is_valid():
        metrolog.save()
        form = NewMetrolog(
            request.POST or None,
            files=request.FILES or None,
            instance=metrolog)
        return redirect('train:train_list')

    context = {'form': form,
               'metrolog': metrolog,
               'is_edit': True, }
    return render(request, 'metrolog/metrolog_create.html', context)