from metrolog.models import Measurement, Certificate
from rest_framework import serializers
from train.models import Train, DoneMaiDate, Maintenance, Serial, Cases
from users.models import UserData


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('description',
                  'seral_number',
                  'date_end',
                  'location',
                  'days',
                  'file',
                  'id',
                  'place',)


class CertificateSerializer(serializers.ModelSerializer):
    metrolog = MeasurementSerializer()

    class Meta:
        model = Certificate
        fields = ('file',
                  'name',
                  'id',
                  'default',
                  'metrolog',)


class SerialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serial
        fields = ('serial', 'slug',)


class TrainSerializer(serializers.ModelSerializer):
    serial = SerialSerializer(read_only=True)

    class Meta:
        model = Train
        fields = ('id', 'serial', 'number', 'renter',
                  'mileage', 'mileage_date', 'day_mileage',)


class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = ('type', 'number',)


class DoneMaiDateSerializer(serializers.ModelSerializer):
    maintenance = MaintenanceSerializer(read_only=True)
    train = TrainSerializer(read_only=True)

    class Meta:
        model = DoneMaiDate
        exclude = ('musthave',)


class CaseSerializer(serializers.ModelSerializer):
    train = TrainSerializer(read_only=True)

    class Meta:
        model = Cases
        fields = ('author', 'train', 'name', 'text',)


class TelegramSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ('author', 'telegram',)
