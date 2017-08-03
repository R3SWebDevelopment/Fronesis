from django import forms
from .models import Appointments
from crum import get_current_user


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

