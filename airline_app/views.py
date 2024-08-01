from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Airline, Aircraft
from .serializers import AirlineSerializer, AircraftSerializer

class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        manufacturer_serial_number = request.data.get('manufacturer_serial_number')
        if manufacturer_serial_number:
            try:
                aircraft = Aircraft.objects.filter(operator_airline=instance).first()
                if aircraft:
                    aircraft_serializer = AircraftSerializer(aircraft, data=request.data, partial=True)
                    aircraft_serializer.is_valid(raise_exception=True)
                    aircraft_serializer.save()
                    return Response(aircraft_serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "Aircraft not found."}, status=status.HTTP_404_NOT_FOUND)
            except Aircraft.DoesNotExist:
                return Response({"detail": "Aircraft not found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.data)

    def custom_post(self, request, *args, **kwargs):
        aircraft_id = kwargs.get('pk')
        if 'delete_aircraft' in request.data:
            return self.delete_aircraft(request, aircraft_id)
        return self.delete_airline(request, *args, **kwargs)

    def delete_aircraft(self, request, aircraft_id):
        try:
            aircraft = Aircraft.objects.get(id=aircraft_id)
            aircraft.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Aircraft.DoesNotExist:
            return Response({"detail": "Aircraft not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete_airline(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
