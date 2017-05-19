from django import forms
from .models import Event, ShoppingCart, TicketSelection
from django.forms.models import modelformset_factory
from django.conf import settings


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        if instance is not None:
            required_fields = ['name', 'subtitle', 'begins_date', 'begins_time', 'ends_date', 'ends_time',
                               'description', 'cover', 'address', 'neighborhood', 'city', 'postal_code']
        else:
            required_fields = ['name', 'begins_date', 'begins_time', 'ends_date', 'ends_time', 'description', 'cover',
                               'address', 'neighborhood', 'city', 'postal_code']
        for field in self.fields:
            if field in required_fields:
                self.fields[field].required = True
            else:
                self.fields[field].required = False
        for field in ['published']:
            self.fields[field].widget.attrs['class'] = 'hide'
        for field in ['ends_time', 'begins_time']:
            self.fields[field].valid_time_formats = settings.VALID_TIME_FORMATS


class EventGetTicketForm(forms.ModelForm):
    credit_card_number = forms.CharField(label='Credit Card Number', required=True, initial="")
    credit_card_exp_month = forms.CharField(label='Expiration Month', required=True, initial="")
    credit_card_exp_year = forms.CharField(label='Expiration Year', required=True, initial="")
    credit_card_cvv = forms.CharField(label='CVV', required=True, initial='')

    class Meta:
        model = ShoppingCart
        fields = '__all__'
        exclude = ['buyer', 'event']


class TicketSelectionForm(forms.ModelForm):
    ticket_label = forms.CharField(required=False)
    price_label = forms.CharField(required=False)
    total_label = forms.CharField(required=False)

    class Meta:
        model = TicketSelection
        fields = ['qty']

    def __init__(self, *args, **kwargs):
        super(TicketSelectionForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        if instance is not None:
            self.fields['ticket_label'].initial = instance.ticket_type.name
            self.fields['price_label'].initial = instance.ticket_type.price
            available_tickets = ((v, v) for v in range(0, instance.ticket_type.available + 1))
            self.fields['qty'].widget = forms.Select(choices=available_tickets, attrs={'class': 'qty_input'})
            self.fields['total_label'].initial = instance.ticket_type.price * instance.qty

    def save(self, commit=True, *args, **kwargs):
        ticket = super(TicketSelectionForm, self).save(commit=False, *args, **kwargs)
        if ticket.qty > 0:
            ticket.select_ticket()


TicketSelectionFormSet = modelformset_factory(form=TicketSelectionForm, model=TicketSelection, extra=0)
