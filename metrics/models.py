from django.db import models

# Create your models here.

class HealthMetric(models.Model):
    METRIC_CHOICES = [
        ('heart_rate', 'Heart Rate'),
        ('oxygen_spo2', 'Oxygen - SpO2'),
        ('steps', 'Steps'),
        ('resting_heart_rate', 'Resting Heart Rate'),
        ('sleep', 'Sleep'),
        ('exercise', 'Exercises'),
        ('stress', 'Stress'),
        # Add other metric choices here
    ]

    metric = models.CharField(max_length=100, choices=METRIC_CHOICES)
    time = models.DateTimeField()
    value = models.FloatField()
