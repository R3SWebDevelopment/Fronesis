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

from django.contrib.sites.models import Site

OAUTH2CALLBACK = '/google/oauth2callback/'
SITE = Site.objects.get_current()
DOMAIN = 'http://{}'.format(SITE.domain) if SITE else 'http://local.test.com'

SESSION_GOOGLE_SUCESS_URL_KEY = 'GOOGLE_SUCESS_URL'
SESSION_GOOGLE_ERROR_URL_KEY = 'GOOGLE_ERROR_URL'

FLOW = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    scope = 'https://www.googleapis.com/auth/calendar',
    redirect_uri='{}{}'.format(DOMAIN, OAUTH2CALLBACK)
)


@login_required
def auth_return(request):
    sucess_url = '{}'.format(request.session[SESSION_GOOGLE_SUCESS_URL_KEY] or '/')
    error_url = '{}'.format(request.session[SESSION_GOOGLE_ERROR_URL_KEY] or '/')
    del request.session[SESSION_GOOGLE_SUCESS_URL_KEY]
    del request.session[SESSION_GOOGLE_ERROR_URL_KEY]

    state = request.GET.get('state', None)
    state = str.encode(state)
    if not xsrfutil.validate_token(settings.SECRET_KEY, state, request.user):
        return HttpResponseBadRequest()
    try:
        credential = FLOW.step2_exchange(request.GET)
    except:
        return HttpResponseRedirect(error_url)
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    return HttpResponseRedirect(sucess_url)


@login_required
def add_appointment(request, pk):
    request.session[SESSION_GOOGLE_SUCESS_URL_KEY] = reverse('google:add_appointment', kwargs={
        'pk': pk
    })
    request.session[SESSION_GOOGLE_ERROR_URL_KEY] = reverse('booking:calendar_view')
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    coach = request.user.coaches.first()
    appointment = coach.appointments.filter(pk=pk).first()
    if coach and appointment:
        http = credential.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        google_calendar_id = coach.google_calendar_id or 'primary'
        event_data = appointment.google_calendar_data
        try:
            event = service.events().insert(calendarId=google_calendar_id, sendNotifications=True,
                                            body=event_data).execute()
            htmlLink = event.get('htmlLink', None)
            if htmlLink:
                appointment.google_calendar_url = htmlLink
                appointment.save()
        except Exception as e:
            print("Exception: {}".format(e))
    return HttpResponseRedirect(reverse('booking:calendar_view'))


@login_required
def connect_calender(request):
    request.session[SESSION_GOOGLE_SUCESS_URL_KEY] = reverse('google:calendar_connect')
    request.session[SESSION_GOOGLE_ERROR_URL_KEY] = reverse('coaches:booking_settings')
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
