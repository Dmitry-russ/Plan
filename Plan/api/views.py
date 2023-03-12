from datetime import datetime

from django.db.models import Max
from rest_framework import viewsets
from train.models import DoneMaiDate, Train, Cases, Maintenance

from .permissions import IsStaff
from .serializers import (DoneMaiDateSerializer,
                          TrainSerializer,
                          CaseSerializer,
                          MaintenanceSerializer, )


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
        wintersummer = self.kwargs.get("wintersummer")
        currentYear = datetime.now().year
        if wintersummer:
            if wintersummer == 'summer':
                wintersummer = 'Лето'
            elif wintersummer == 'winter':
                wintersummer = 'Зима'
            return (DoneMaiDate.objects.
                    filter(maintenance__type=wintersummer,
                           maintenance_date__year=currentYear).
                    order_by('-maintenance_date'))
        return (DoneMaiDate.objects.
                    filter(train__number=number, train__serial__slug=serial).
                    order_by('-mileage')[:3])


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
