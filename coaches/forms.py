from django import forms
from .models import Coach
from django.contrib.auth.models import User


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
