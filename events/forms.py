from django.forms import ModelForm
from .models import Event


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

