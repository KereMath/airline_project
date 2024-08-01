from django.db import models

class Airline(models.Model):
    name = models.CharField(max_length=100)
    callsign = models.CharField(max_length=100)
    founded_year = models.IntegerField()
    base_airport = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Aircraft(models.Model):
    manufacturer_serial_number = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    operator_airline = models.ForeignKey(Airline, related_name='aircraft_set', on_delete=models.CASCADE)
    number_of_engines = models.IntegerField()

    def __str__(self):
        return self.model
