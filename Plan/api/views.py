from train.models import DoneMaiDate
from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated

from .serializers import (DoneMaiDateSerializer)


class DoneMaiDateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DoneMaiDateSerializer
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        number = self.kwargs.get("number")
        return (DoneMaiDate.objects.
                filter(train__number=number).order_by('-mileage')[:3])
