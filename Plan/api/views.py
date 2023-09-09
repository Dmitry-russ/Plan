from datetime import datetime, timedelta

from django.db.models import Max
from metrolog.models import Measurement, Certificate
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from train.models import DoneMaiDate, Train, Cases, Maintenance

from .permissions import IsStaff
from .serializers import (DoneMaiDateSerializer,
                          TrainSerializer,
                          CaseSerializer,
                          MaintenanceSerializer,
                          MeasurementSerializer,
                          CertificateSerializer, )

DAYS_GORISONT = 90
MAI_REPORT_COUNT = 4


class CertificateSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CertificateSerializer
    permission_classes = (IsStaff,)

    def get_queryset(self):
        return Certificate.objects.filter(
            metrolog__id=self.kwargs.get('id'), default=True)


class MeasurementSet(viewsets.ReadOnlyModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = (IsStaff,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['description', 'seral_number']
    ordering_fields = ['location', ]
    ordering = ['location', ]

    @action(detail=True, methods=["GET"], )
    def measurement(self, request, pk):
        """Запрос одного СИ."""
        data = get_object_or_404(Measurement, id=pk)
        return data


class MaiNumViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MaintenanceSerializer
    permission_classes = (IsStaff,)

    def get_queryset(self):
        last_mai = Maintenance.objects.aggregate(Max('number'))
        number = int(self.kwargs.get("number"))
        if number > last_mai['number__max']:
            number = 1
        next_mai = Maintenance.objects.filter(number=number)
        if next_mai:
            return next_mai


class DoneMaiDateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DoneMaiDateSerializer
    permission_classes = (IsStaff,)

    def get_queryset(self):
        serial = self.kwargs.get("serial")
        number = self.kwargs.get("number")
        info = self.kwargs.get("info")
        currentYear = datetime.now().year
        currentDate = datetime.today()
        days30Date = currentDate - timedelta(days=DAYS_GORISONT)
        choose_report: dict = {
            'summer': 'Лето',
            'winter': 'Зима'
        }
        if info:
            if info == '30days':
                return (DoneMaiDate.objects.
                        filter(
                    maintenance_date__range=[days30Date, currentDate]).
                        order_by('-maintenance_date'))
            return (DoneMaiDate.objects.
                    filter(maintenance__type=choose_report.get(info),
                           maintenance_date__year=currentYear).
                    order_by('-maintenance_date'))
        return (DoneMaiDate.objects.
                    filter(train__number=number, train__serial__slug=serial).
                    order_by('-mileage')[:MAI_REPORT_COUNT])


class TrainViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TrainSerializer
    permission_classes = (IsStaff,)

    def get_queryset(self):
        number = self.kwargs.get("number")
        if number:
            return (Train.objects.
                    filter(number=number).order_by('serial'))
        return (Train.objects.all())


class CaseViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CaseSerializer
    permission_classes = (IsStaff,)

    def get_queryset(self):
        number = self.kwargs.get("number")
        serial = self.kwargs.get("serial")
        # train = Train.objects.filter(number=number, serial__serial=serial)

        return (Cases.objects.
                filter(train__serial__slug=serial, train__number=number))
