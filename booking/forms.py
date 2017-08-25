from django import forms
from .models import Appointments, AppointmentRequest
from crum import get_current_user
from events.models import STATE_CHOICES


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


class CreditCardForm(forms.Form):
    first_name = forms.CharField(label='First Name', required=True, initial="")
    last_name = forms.CharField(label='Last Name', required=True, initial="")
    email = forms.EmailField(label='E-Mail', required=True, initial="")
    line1 = forms.CharField(label='Address Line 1', required=True, initial="")
    line2 = forms.CharField(label='Address Line 2', required=False, initial="")
    line3 = forms.CharField(label='Address Line 2', required=False, initial="")
    city = forms.CharField(label='City', required=True, initial="")
    state = forms.ChoiceField(label='State', required=True, initial="", choices=STATE_CHOICES)
    phone_number = forms.CharField(label='Phone Number', required=True, initial="")
    postal_code = forms.IntegerField(label='Postal Code', required=True, initial="")
    amount = forms.DecimalField(label="Amount", required=True, initial="")
    order = forms.IntegerField(required=True, initial="", widget=forms.HiddenInput())
    description = forms.CharField(required=True, initial="", widget=forms.HiddenInput())
    credit_card_number = forms.CharField(label='Credit Card Number', required=True, initial="")
    credit_card_exp_month = forms.CharField(label='Expiration Month', required=True, initial="")
    credit_card_exp_year = forms.CharField(label='Expiration Year', required=True, initial="")
    credit_card_cvv = forms.CharField(label='CVV', required=True, initial='')

