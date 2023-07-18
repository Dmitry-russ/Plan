import tablib
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import NewMetrolog, FilterForm, NewCertificate
from .models import Measurement, Certificate

MEDIA_URL = settings.MEDIA_URL

"переменные для отрисвоки цвета поля оставшихся дней"
WARNING_DAYS = 90
DANGER_DAYS = 45


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
    return redirect('metrolog:metrolog_small_report')


@login_required
def certificate_create(request, metrolog_id):
    """Прикрепление сертификата."""

    metrolog = get_object_or_404(Measurement, id=metrolog_id)
    certificates = Certificate.objects.filter(metrolog=metrolog)
    form = NewCertificate(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(
            request,
            'metrolog/metrolog_certificate_create.html',
            {'form': form,
             'is_edit': False,
             "certificates": certificates,
             "metrolog": metrolog,
             "media": MEDIA_URL, }
        )
    certificate = form.save(commit=False)
    certificate.author = request.user
    certificate.metrolog = metrolog
    certificate.save()
    return redirect('metrolog:certificate_create', metrolog_id=metrolog_id)


@login_required
def certificate_delete(request, certificate_id):
    """Удаление сертификата."""

    certificate = get_object_or_404(Certificate, id=certificate_id)
    metrolog_id = certificate.metrolog.id
    certificate.delete()
    return redirect('metrolog:certificate_create', metrolog_id=metrolog_id)


@login_required
def certificate_default(request, certificate_id):
    """Изменение актуальности сертификата."""

    certificate = get_object_or_404(Certificate, id=certificate_id)
    metrolog_id = certificate.metrolog.id
    if certificate.default:
        certificate.default = False
        certificate.save()
        return redirect('metrolog:certificate_create', metrolog_id=metrolog_id)
    certificate.default = True
    certificate.save()
    return redirect('metrolog:certificate_create', metrolog_id=metrolog_id)


@login_required
def metrolog_detail(request, metrolog_id):
    """Изменение инструмента СИ."""

    metrolog = get_object_or_404(Measurement, id=metrolog_id)
    certificates = Certificate.objects.filter(metrolog=metrolog, default=True)

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
        return redirect('metrolog:metrolog_detail', metrolog_id=metrolog.id)

    context = {'form': form,
               'metrolog': metrolog,
               'is_edit': True,
               'certificates': certificates,
               'media': MEDIA_URL,
               }
    return render(request, 'metrolog/metrolog_create.html', context)


@login_required
def metrolog_small_report(request):
    """Краткий отчет по метрологии."""

    metrolog = Measurement.objects.all().order_by('description')

    filter_form = FilterForm(request.GET)
    if filter_form.is_valid():
        if filter_form.cleaned_data["location"]:
            metrolog = metrolog.filter(
                location=filter_form.cleaned_data["location"])
        if filter_form.cleaned_data["place"]:
            metrolog = metrolog.filter(
                place__icontains=filter_form.cleaned_data["place"])
        if filter_form.cleaned_data["seral_number"]:
            metrolog = metrolog.filter(
              seral_number__icontains=filter_form.cleaned_data["seral_number"])
        if filter_form.cleaned_data["description"]:
            metrolog = metrolog.filter(
              description__icontains=filter_form.cleaned_data["description"])

    NewMetrologFormSet = modelformset_factory(
        Measurement, form=NewMetrolog, extra=0)
    formset = NewMetrologFormSet(
        request.POST or None,
        files=request.FILES or None,
        queryset=metrolog)

    if formset.is_valid():
        formset.save()
        formset = NewMetrologFormSet(
            request.POST or None,
            files=request.FILES or None,
            queryset=metrolog)
        messages.success(request, 'Данные сохранены.')
        return redirect('metrolog:metrolog_small_report')
    check_form: bool = formset.is_valid()
    context = {'formset': formset,
               'metrolog': metrolog,
               'check_form': check_form,
               'warning_days': WARNING_DAYS,
               'danger_days': DANGER_DAYS,
               'filter_form': filter_form,
               }
    return render(request, 'metrolog/metrolog_small_list.html', context)


@login_required
def mai_export(request):
    """Выгрузка в файл списка СИ."""

    metrolog = Measurement.objects.all().order_by('id')
    headers = (
        'Тип СИ',
        'Номер DU',
        'Описание',
        'Локация',
        'Модель СИ',
        'Производитель',
        'Номер в госреестре',
        'Тип метрологического контроля',
        'Периодичность проверки, мес.',
        'Организация для направления в поверку',
        'Фактическая организация, проводившая поверку',
        'Серийный номер',
        'Дата проверки',
        'Дата окончания поверки',
        'Фактическое местоположение',
        'Наличие в акте РЖД',
        'Примечание',
        'Дней до конца поверки',
    )
    data = []
    data = tablib.Dataset(*data, headers=headers)
    for metr in metrolog:
        data.append([
            metr.type,
            metr.dunumber,
            metr.description,
            metr.location,
            metr.model,
            metr.maker,
            metr.number,
            metr.control_type,
            metr.periodicity,
            metr.organization,
            metr.organization_fact,
            metr.seral_number,
            metr.date_control,
            metr.date_end,
            metr.place,
            metr.in_act,
            metr.note,
            metr.get_days(),
        ])
    response = HttpResponse(
        data.export('xls'),
        content_type='application/vnd.ms-excel;charset=utf-8')
    text = "attachment; filename=BaseSI.xls"
    response['Content-Disposition'] = text
    return response
