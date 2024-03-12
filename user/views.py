from django.shortcuts import render, redirect
from django.urls import reverse
from google_auth_oauthlib.flow import Flow
from django.conf import settings

SCOPES = ['https://www.googleapis.com/auth/fitness.activity.read']

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
    print("I am here")
    state = request.session['google_fit_state']
    flow = Flow.from_client_secrets_file('client_secret.json', SCOPES, state=state)
    flow.redirect_uri = request.build_absolute_uri(reverse('user:callback_google_fit'))
    flow.fetch_token(authorization_response="http://127.0.0.1:8000")
    request.session["google_fit_credentials"] = flow.credentials
    print(flow.credentials)
    redirect(reverse("metrics:heartrate"))