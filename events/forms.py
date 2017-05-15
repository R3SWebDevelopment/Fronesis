from django import forms
from .models import Event, PaymentCustomer

from django.conf import settings


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        if instance is not None:
            required_fields = ['name', 'subtitle', 'begins_date', 'begins_time', 'ends_date', 'ends_time', 'description', 'cover',
                               'address', 'neighborhood', 'city', 'postal_code']
        else:
            required_fields = ['name', 'begins_date', 'begins_time', 'ends_date', 'ends_time', 'description', 'cover',
                               'address', 'neighborhood', 'city', 'postal_code']
        for field in self.fields:
            if field in required_fields:
                self.fields[field].required = True
            else:
                self.fields[field].required = False
        for field in ['ends_time', 'begins_time']:
            self.fields[field].valid_time_formats = settings.VALID_TIME_FORMATS


class PaymentForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    line1 = forms.CharField(required=True)
    line2 = forms.CharField(required=True)
    line3 = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
