from django import forms
from .models import Coach, AVAILABLE_HOURS, AvailableHour, Venue
from django.contrib.auth.models import User
from crum import get_current_user


class CoachContactForm(forms.ModelForm):
    full_name = forms.CharField()
    email = forms.CharField()

    class Meta:
        model = Coach
        fields = ['full_name', 'email', 'specialty', 'office_phone', 'mobile_phone', 'job_title', 'current_city',
                  'default_skype_id']

    def __init__(self, *args, **kwargs):
        super(CoachContactForm, self).__init__(*args, **kwargs)
        instance = self.instance
        self.fields['full_name'].initial = instance.user.get_full_name()
        self.fields['email'].initial = instance.user.email
        for field in ['specialty', 'office_phone', 'mobile_phone', 'job_title', 'current_city', 'default_skype_id']:
            self.fields[field].required = False

    def clean_email(self):
        email = self.cleaned_data['email']
        instance = self.instance
        if instance:
            qs = User.objects.exclude(pk=instance.pk).filter(email__iexact=email)
        else:
            qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError('La dirección de correo {} ya ha sido registrada'.format(email))
        return email

    def save(self, commit=True):
        instance = super(CoachContactForm, self).save(commit=True)
        email = self.cleaned_data['email']
        full_name = self.cleaned_data['full_name']
        user = instance.user
        user.emai = email
        name = full_name.split(' ')
        first_name = name[0]
        last_name = ' '.join(name[1:])
        user.first_name = first_name
        user.last_name = last_name
        user.save()


class CoachBlockedHours(forms.ModelForm):
    sunday = forms.MultipleChoiceField(choices=AVAILABLE_HOURS)
    monday = forms.MultipleChoiceField(choices=AVAILABLE_HOURS)
    tuesday = forms.MultipleChoiceField(choices=AVAILABLE_HOURS)
    wednesday = forms.MultipleChoiceField(choices=AVAILABLE_HOURS)
    thursday = forms.MultipleChoiceField(choices=AVAILABLE_HOURS)
    friday = forms.MultipleChoiceField(choices=AVAILABLE_HOURS)
    saturday = forms.MultipleChoiceField(choices=AVAILABLE_HOURS)

    class Meta:
        model = Coach
        fields = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

    def __init__(self, *args, **kwargs):
        super(CoachBlockedHours, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'hidden'
            self.fields[field].required = False
            if instance:
                self.fields[field].initial = AvailableHour.get_hours(coach=instance, day_name=field)

    def save(self, commit=False):
        instance = super(CoachBlockedHours, self).save(commit=False)
        days = []
        days.append(self.cleaned_data.get('sunday', []))
        days.append(self.cleaned_data.get('monday', []))
        days.append(self.cleaned_data.get('tuesday', []))
        days.append(self.cleaned_data.get('wednesday', []))
        days.append(self.cleaned_data.get('thursday', []))
        days.append(self.cleaned_data.get('friday', []))
        days.append(self.cleaned_data.get('saturday', []))
        instance.available_hours.all().delete()
        day = 0
        for day_hours in days:
            for hour in day_hours:
                if hour not in ['ALL']:
                    try:
                        hour = int(int(hour) / 100)
                    except ValueError:
                        hour = None
                    if hour:
                        AvailableHour.objects.get_or_create(coach=instance, day=day, hour=hour)
            day += 1


class CoachBookingSettings(forms.ModelForm):
    google_calendar = forms.ChoiceField(required=False)

    class Meta:
        model = Coach
        fields = ['is_instante_booking_allow', 'ask_before_booking', 'google_calendar']

    def __init__(self, *args, **kwargs):
        super(CoachBookingSettings, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        for field in ['is_instante_booking_allow', 'ask_before_booking']:
            self.fields[field].widget = forms.CheckboxInput()
        if instance:
            if instance.is_google_account_set:
                self.fields['google_calendar'].choices = instance.get_google_calendar_list_choices

    def save(self, commit=False):
        instance = super(CoachBookingSettings, self).save(commit=False)
        google_calendar = self.cleaned_data.get('google_calendar', None)
        instance.google_calendar_id = google_calendar
        instance.save()


class VenuesForm(forms.ModelForm):

    class Meta:
        model = Venue
        fields = ['coach', 'name', 'address']

    def __init__(self, *args, **kwargs):
        super(VenuesForm, self).__init__(*args, **kwargs)
        self.fields['coach'].initial = get_current_user().coaches.first()
        self.fields['coach'].widget = forms.HiddenInput()
