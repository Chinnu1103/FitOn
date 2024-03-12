from django.urls import path
from .views import get_heart_rate

app_name="metrics"
urlpatterns = [
    path('heartrate/', get_heart_rate, name='get_heart_rate'),
]