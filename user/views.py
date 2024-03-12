from django.shortcuts import render, redirect
from django.urls import reverse
from google_auth_oauthlib.flow import Flow
from django.conf import settings

SCOPES = [
    'https://www.googleapis.com/auth/fitness.activity.read', 
    'https://www.googleapis.com/auth/fitness.body.read', 
    'https://www.googleapis.com/auth/fitness.heart_rate.read', 
    'https://www.googleapis.com/auth/fitness.sleep.read',
    'https://www.googleapis.com/auth/fitness.blood_glucose.read',
    'https://www.googleapis.com/auth/fitness.blood_pressure.read',
    'https://www.googleapis.com/auth/fitness.body_temperature.read',
    'https://www.googleapis.com/auth/fitness.location.read',
    'https://www.googleapis.com/auth/fitness.nutrition.read',
    'https://www.googleapis.com/auth/fitness.oxygen_saturation.read',
    'https://www.googleapis.com/auth/fitness.reproductive_health.read'
]

def authorize_google_fit(request):
    credentials = request.session.get('google_fit_credentials')

    if not credentials or credentials.expired:
        flow = Flow.from_client_config(settings.GOOGLEFIT_CLIENT_CONFIG, SCOPES)
        flow.redirect_uri = request.build_absolute_uri(reverse('user:callback_google_fit'))
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        request.session['google_fit_state'] = state

    return redirect(authorization_url)

def callback_google_fit(request):
    state = request.session['google_fit_state']
    
    if state:
        flow = Flow.from_client_config(settings.GOOGLEFIT_CLIENT_CONFIG, SCOPES, state=state)
        flow.redirect_uri = request.build_absolute_uri(reverse('user:callback_google_fit'))
        flow.fetch_token(authorization_response = request.build_absolute_uri())
        
        credentials = flow.credentials
        request.session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        
    return redirect(reverse("metrics:get_heart_rate"))