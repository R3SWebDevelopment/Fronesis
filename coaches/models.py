from django.db import models
from django.contrib.auth.models import User

DAYS = (
    (0, 'Sunday'),
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
)


class Coach(models.Model):
    user = models.ForeignKey(User, null=False)
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
    sunday_works = models.BooleanField(default=False)
    monday_works = models.BooleanField(default=False)
    tuesday_works = models.BooleanField(default=False)
    wednesday_works = models.BooleanField(default=False)
    thursday_works = models.BooleanField(default=False)
    friday_works = models.BooleanField(default=False)
    saturday_works = models.BooleanField(default=False)


class AvailableHour(models.Model):
    coach = models.ForeignKey(Coach, null=False)
    day = models.IntegerField(default=0, choices=DAYS)
    hour = models.IntegerField(default=0)


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

