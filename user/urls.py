from django.urls import path
from .views import authorize_google_fit, callback_google_fit

app_name="user"
urlpatterns = [
    path('callback/', callback_google_fit, name='callback_google_fit'),
    path('authorize/', authorize_google_fit, name='authorize_googlefit'),
]