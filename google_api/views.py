import os
import logging
import httplib2

from googleapiclient.discovery import build
from apiclient import discovery
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import CredentialsModel
from django.conf import settings

from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_util.storage import DjangoORMStorage

from django.urls import reverse

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>


def get_flow():
    oauth2callback = '/google/oauth2callback/'
    flow = flow_from_clientsecrets(
        settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
        scope='https://www.googleapis.com/auth/calendar',
        redirect_uri='http://fronesis.vordem.mx{}'.format(oauth2callback))
    return flow


@login_required
def auth_return(request):
    FLOW = get_flow()
    state = request.GET.get('state', None)
    state = str.encode(state)
    if not xsrfutil.validate_token(settings.SECRET_KEY, state, request.user):
        return HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.GET)
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    return HttpResponseRedirect("/google/calendar/connect/")


@login_required
def connect_calender(request):
    FLOW = get_flow()
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    coach = request.user.coaches.first()
    if coach:
        http = credential.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        acl_data = service.acl().list(calendarId='primary').execute()
        items = acl_data.get('items', [])
        if len(items) > 0:
            request.user.coaches.first().connect_google_account(items[0])
            calendars_data = service.calendarList().list(pageToken=None).execute()
            request.user.coaches.first().set_google_calender_list(calendars_data.get('items', []))
    return HttpResponseRedirect(reverse('coaches:booking_settings'))


@login_required
def disconnect_calender(request):
    CredentialsModel.objects.filter(id=request.user).delete()
    request.user.coaches.first().disconnect_google_account()
    return HttpResponseRedirect(reverse('coaches:booking_settings'))
