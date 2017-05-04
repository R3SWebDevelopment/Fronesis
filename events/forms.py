from django.forms import ModelForm
from .models import Event

from django.conf import settings


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        if instance is not None:
            required_fields = []
        else:
            required_fields = []
        for field in self.fields:
            if field in required_fields:
                self.fields[field].required = True
            else:
                self.fields[field].required = False
        for field in ['ends_time', 'begins_time']:
            self.fields[field].valid_time_formats = settings.VALID_TIME_FORMATS
