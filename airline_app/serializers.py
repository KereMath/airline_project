from rest_framework import serializers
from .models import Airline, Aircraft

class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = '__all__'

class AirlineSerializer(serializers.ModelSerializer):
    aircraft_set = AircraftSerializer(many=True, read_only=True)

    class Meta:
        model = Airline
        fields = '__all__'
