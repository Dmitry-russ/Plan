from train.models import DoneMaiDate, Maintenance
from rest_framework import serializers


# class TrainSerializer(serializers.ModelSerializer):

#     author = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Train
#         fields = ('id', 'serial', 'number', 'renter',
#                   'mileage', 'mileage_date', 'day_mileage',)
class MaintenanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Maintenance
        fields = ('type',)


class DoneMaiDateSerializer(serializers.ModelSerializer):

    maintenance = MaintenanceSerializer(read_only=True)

    class Meta:
        model = DoneMaiDate
        exclude = ('musthave',)
