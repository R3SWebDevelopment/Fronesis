from django import forms
from .models import Appointments, AppointmentRequest
from crum import get_current_user


class AppointmentRequestConfirmForm(forms.ModelForm):

    class Meta:
        model = AppointmentRequest
        fields = ['id']

    def save(self, commit=False):
        instance = super(AppointmentRequestConfirmForm, self).save(commit=False)
        appointment = Appointments.objects.create(coach=instance.coach, starts_datetime=instance.starts_datetime,
                                                  ends_datetime=instance.ends_datetime,
                                                  online_call=instance.online_call, venue=instance.venue,
                                                  client=instance.client, service=instance.service, already_paid=False,
                                                  send_payment_link=False)
        return appointment


class AddAppointmentForm(forms.ModelForm):
    client_full_name = forms.CharField()
    client_email = forms.CharField()

    class Meta:
        model = Appointments
        fields = ['coach', 'client', 'client_full_name', 'client_email']

    def __init__(self, *args, **kwargs):
        super(AddAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['coach'].widget = forms.HiddenInput()
        self.fields['client'].required = False

