from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

DAYS = (
    (0, 'Sunday'),
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
)


AVAILABLE_HOURS = (
    ('ALL', 'Check all'),
    ('0700', '7:00 am'),
    ('0800', '8:00 am'),
    ('0900', '9:00 am'),
    ('1000', '10:00 am'),
    ('1100', '11:00 am'),
    ('1200', '12:00 pm'),
    ('1300', '1:00 pm'),
    ('1400', '2:00 pm'),
    ('1500', '3:00 pm'),
    ('1600', '4:00 pm'),
    ('1700', '5:00 pm'),
    ('1800', '6:00 pm'),
    ('1900', '7:00 pm'),
    ('2000', '8:00 pm'),
    ('2100', '9:00 pm'),
)


class Coach(models.Model):
    user = models.ForeignKey(User, null=False, related_name='coaches')
    specialty = models.CharField(max_length=150, null=False, default='')
    office_phone = models.CharField(max_length=10, null=False, default='')
    mobile_phone = models.CharField(max_length=10, null=False, default='')
    job_title = models.CharField(max_length=150, null=True, default=None)
    current_city = models.CharField(max_length=150, null=False, default='')
    default_skype_id = models.CharField(max_length=50, null=False, default='')
    is_instante_booking_allow = models.BooleanField(default=False)
    ask_before_booking = models.BooleanField(default=False)
    google_calendar_account_id = models.CharField(max_length=50, null=False, default='')
    google_calendar_id = models.CharField(max_length=50, null=False, default='')
    google_calender_list = JSONField(null=True, default=None)
    sunday_works = models.BooleanField(default=False)
    monday_works = models.BooleanField(default=False)
    tuesday_works = models.BooleanField(default=False)
    wednesday_works = models.BooleanField(default=False)
    thursday_works = models.BooleanField(default=False)
    friday_works = models.BooleanField(default=False)
    saturday_works = models.BooleanField(default=False)

    @property
    def is_google_account_set(self):
        return True if self.google_calendar_account_id else False

    def connect_google_account(self, data=None):
        if data:
            google_calendar_account_id = data.get('id', None)
            if google_calendar_account_id:
                self.google_calendar_account_id = google_calendar_account_id
                self.save()

    def set_google_calender_list(self, calender_list=None):
        if calender_list:
            self.google_calender_list = calender_list
            self.save()


class AvailableHour(models.Model):
    coach = models.ForeignKey(Coach, null=False, related_name='available_hours')
    day = models.IntegerField(default=0, choices=DAYS)
    hour = models.IntegerField(default=0)

    @classmethod
    def get_hours(cls, coach=None, day_name=None):
        day = None
        if day_name == 'sunday':
            day = 0
        elif day_name == 'monday':
            day = 1
        elif day_name == 'tuesday':
            day = 2
        elif day_name == 'wednesday':
            day = 3
        elif day_name == 'thursday':
            day = 4
        elif day_name == 'friday':
            day = 5
        elif day_name == 'saturday':
            day = 6
        if coach and day:
            return ['0{}00'.format(h.get('hour')) if h.get('hour') < 10 else '{}00'.format(h.get('hour'))
                    for h in cls.objects.filter(coach=coach).filter(day=day).values('hour')]
        return []


class Venue(models.Model):
    coach = models.ForeignKey(Coach, null=False)
    name = models.CharField(max_length=150, null=False, default='')
    address = models.TextField(null=False)


class Session(models.Model):
    coach = models.ForeignKey(Coach, null=False)
    name = models.CharField(max_length=150, null=False, default='')
    length_hours = models.IntegerField(default=0)
    length_minutes = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(null=False)
    category = models.CharField(max_length=150, null=False, default='')
    face_to_face = models.BooleanField(default=False)
    all_venues = models.BooleanField(default=False)
    allow_on_venues = models.ManyToManyField(Venue)
    one_on_one = models.BooleanField(default=False)
    groups_allow = models.BooleanField(default=False)
    person_price = models.DecimalField(max_digits=8, decimal_places=2)
    max_capacity = models.IntegerField(default=0)


class Bundle(models.Model):
    coach = models.ForeignKey(Coach, null=False)
    name = models.CharField(max_length=150, null=False, default='')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(null=False)
    category = models.CharField(max_length=150, null=False, default='')
    number_sessions = models.BooleanField(default=False)
    upfront_payment_required = models.BooleanField(default=False)
    down_payment_allow = models.BooleanField(default=False)
    down_payment = models.DecimalField(max_digits=8, decimal_places=2)
    expires = models.BooleanField(default=False)
    expiration_date = models.DateField(null=True, verbose_name="ends")

