from rest_framework import viewsets
from train.models import DoneMaiDate, Train, Cases
from django.shortcuts import get_object_or_404

from .permissions import IsStaff
from .serializers import (DoneMaiDateSerializer,
                          TrainSerializer,
                          CaseSerializer,)


class DoneMaiDateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DoneMaiDateSerializer
    permission_classes = (IsStaff,)

    def get_queryset(self):
        number = self.kwargs.get("number")
        serial = self.kwargs.get("serial")
        return (DoneMaiDate.objects.
                filter(train__number=number, train__serial__slug=serial).
                order_by('-mileage')[:3])


class TrainViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TrainSerializer
    permission_classes = (IsStaff,)

    def get_queryset(self):
        number = self.kwargs.get("number")
        return (Train.objects.
                filter(number=number).order_by('serial'))


class CaseViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CaseSerializer
    permission_classes = (IsStaff,)

    def get_queryset(self):
        number = self.kwargs.get("number")
        serial = self.kwargs.get("serial")
        # train = Train.objects.filter(number=number, serial__serial=serial)

        return (Cases.objects.
                filter(train__serial__slug=serial, train__number=number ))
