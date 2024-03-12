from django.urls import path
from .views import get_metric_data, list_metrics

app_name="metrics"
urlpatterns = [
    path('data/<str:metric>/', get_metric_data, name='get_metric_data'),
    path('list/', list_metrics, name='list_metrics'),
]