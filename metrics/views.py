from django.shortcuts import render, redirect
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from user.views import authorize_google_fit
import time

def get_heart_rate(request):
    # if request.user.is_authenticated:
    credentials = authorize_google_fit(request)
    service = build('fitness', 'v1', credentials=credentials)
    
    data = service.users().dataset().aggregate(userId='me', body={
        "aggregateBy": [{"dataTypeName": "com.google.heart_rate.bpm"}],
        "bucketByTime": {"durationMillis": 86400000},
        "startTimeMillis": (int(time.time()) - 86400 * 1000 * 10),
        "endTimeMillis": int(time.time()),
    }).execute()
    
    return render(request, 'heart_rate.html', {'data': data})
