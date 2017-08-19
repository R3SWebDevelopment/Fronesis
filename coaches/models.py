from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from datetime import datetime
from philios.models import Post
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from crum import get_current_user
from django_comments.models import Comment

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

LENGTH_HOUR_CHOICES = (
    (h, '{} hours'.format(h)) if h > 1 else (h, '{} hour'.format(h)) for h in range(17)
)

LENGTH_MINUTE_CHOICES = (
    (m, '{} minutes'.format(m)) if m > 1 else (m, '{} minute'.format(m)) for m in range(60)
)


class Client(models.Model):
    full_name = models.CharField(max_length=250, null=False, blank=False)
    email = models.EmailField(max_length=250, null=False, blank=False)

    @property
    def sessions_data(self):
        bp = self.appointments.all()
        now = datetime.now()
        return {
            'total': bp.count(),
            'past': bp.filter(ends_datetime__lte=now).count(),
            'upcoming': bp.filter(starts_datetime__gte=now).count(),
        }

    @property
    def bundles_count(self):
        return 0


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
    clients = models.ManyToManyField(Client)
    short_bio = models.TextField(null=False, blank=True, default='')

    @property
    def philios(self):
        user = get_current_user()
        if user :
            mines = Q(user__pk=user.pk)
            content_type = ContentType.objects.get_for_model(Post)
            post_comments = [c.get('object_pk') for c in Comment.objects.filter(content_type=content_type,
                                                                               user__pk=user.pk).values('object_pk')]
            commented = Q(pk__in=post_comments)
            rated = Q(rating__user__pk=user.pk)
            qs = Post.objects.filter(mines | commented | rated).distinct()
        else:
            qs = Post.objects.none()
        return qs

    @property
    def avatar(self):
        profile = self.user.profile
        if profile.userprofile:
            return '/media/{}'.format(profile.userprofile.avatar)
        return 'https://lelakisihat.com/wp-content/uploads/2016/09/avatar.jpg'

    @property
    def full_name(self):
        return self.user.get_full_name or self.user.email

    @property
    def is_google_account_set(self):
        return True if self.google_calendar_account_id else False

    def connect_google_account(self, data=None):
        if data:
            google_calendar_account_id = data.get('scope', {}).get('value', None)
            if google_calendar_account_id:
                self.google_calendar_account_id = google_calendar_account_id
                self.save()

    def disconnect_google_account(self):
        self.google_calender_list = None
        self.google_calendar_account_id = ''
        self.google_calendar_id = ''
        self.save()

    def set_google_calender_list(self, calender_list=None):
        if calender_list:
            self.google_calender_list = calender_list
            self.save()

    @property
    def get_google_calendar_list_choices(self):
        if self.is_google_account_set and self.google_calender_list:
            calendars = (('{}'.format(l.get('id')), '{}'.format(l.get('summary')))
                         for l in self.google_calender_list if l.get('accessRole', None) == 'owner')
            return calendars
        return ()


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
        if coach and day >= 0:
            hours = ['0{}00'.format(h.get('hour')) if h.get('hour') < 10 else '{}00'.format(h.get('hour'))
                     for h in cls.objects.filter(coach=coach).filter(day=day).values('hour')]
            return hours
        return []


class Venue(models.Model):
    coach = models.ForeignKey(Coach, null=False, related_name='venues')
    name = models.CharField(max_length=150, null=False, default='')
    address = models.TextField(null=False)

    def __str__(self):
        return self.name


class Session(models.Model):
    coach = models.ForeignKey(Coach, null=False, related_name="services")
    name = models.CharField(max_length=150, null=False, default='')
    length_hours = models.IntegerField(default=0, choices=LENGTH_HOUR_CHOICES)
    length_minutes = models.IntegerField(default=0, choices=LENGTH_MINUTE_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(null=False)
    category = models.CharField(max_length=150, null=False, default='')
    face_to_face = models.BooleanField(default=False)
    online = models.BooleanField(default=False)
    all_venues = models.BooleanField(default=False)
    allow_on_venues = models.ManyToManyField(Venue)
    one_on_one = models.BooleanField(default=False)
    groups_allow = models.BooleanField(default=False)
    person_price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    max_capacity = models.IntegerField(default=None, null=True)

    @property
    def length(self):
        length = ''
        if self.length_hours:
            length = '{} hours '.format(self.length_hours) \
                if self.length_hours > 1 else '{} hour '.format(self.length_hours)
        if self.length_minutes:
            length += '{} minutes '.format(self.length_minutes) \
                if self.length_minutes > 1 else '{} minute '.format(self.length_minutes)
        return "{} meeting".format(length)

    @property
    def price_label(self):
        length = ''
        if self.length_hours:
            length = '{} hrs '.format(self.length_hours) \
                if self.length_hours > 1 else '{} hr '.format(self.length_hours)
        if self.length_minutes:
            length += '{} min '.format(self.length_minutes) \
                if self.length_minutes > 1 else '{} min '.format(self.length_minutes)
        return '{} / ${} MXN'.format(length, self.price)


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

