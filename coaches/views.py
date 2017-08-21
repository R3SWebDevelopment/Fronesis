from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from .models import Coach, Venue, Session, Bundle
from .forms import CoachContactForm, CoachBlockedHours, CoachBookingSettings, VenuesForm, SessionForm
from crum import get_current_user
from utils.views import FronesisBaseInnerView
from django.core.urlresolvers import reverse
from django.db.models import Q
from datetime import datetime


class ContactDetail(UpdateView, FronesisBaseInnerView):
    model = Coach
    queryset = Coach.objects.all()
    form_class = CoachContactForm
    object = None
    template_name = 'detail.html'
    coach_settings_section = True

    def get_form(self, form_class=None):
        form_class = self.get_form_class()
        form = form_class(instance=self.get_object())
        return form

    def get_object(self, queryset=None):
        user = get_current_user()
        instance, created = Coach.objects.get_or_create(user=user)
        self.object = instance
        return instance

    def get_context_data(self, **kwargs):
        context = super(ContactDetail, self).get_context_data(**kwargs)
        context['contact'] = True
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = form_class(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('coaches:contact_information')


class BlockedHours(UpdateView, FronesisBaseInnerView):
    model = Coach
    queryset = Coach.objects.all()
    form_class = CoachBlockedHours
    object = None
    template_name = 'blocked_hours.html'
    coach_settings_section = True

    def get_form(self, form_class=None):
        form_class = self.get_form_class()
        form = form_class(instance=self.get_object())
        return form

    def get_object(self, queryset=None):
        user = get_current_user()
        instance, created = Coach.objects.get_or_create(user=user)
        self.object = instance
        return instance

    def get_context_data(self, **kwargs):
        context = super(BlockedHours, self).get_context_data(**kwargs)
        context['blocked'] = True
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = form_class(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('coaches:blocked_hours')


class BookingSettings(UpdateView, FronesisBaseInnerView):
    model = Coach
    queryset = Coach.objects.all()
    form_class = CoachBookingSettings
    object = None
    template_name = 'settings.html'
    coach_settings_section = True

    def get_form(self, form_class=None):
        form_class = self.get_form_class()
        form = form_class(instance=self.get_object())
        return form

    def get_object(self, queryset=None):
        user = get_current_user()
        instance, created = Coach.objects.get_or_create(user=user)
        self.object = instance
        return instance

    def get_context_data(self, **kwargs):
        context = super(BookingSettings, self).get_context_data(**kwargs)
        context['settings'] = True
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = form_class(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('coaches:booking_settings')


class MyVenues(ListView, FronesisBaseInnerView):
    model = Venue
    queryset = Venue.objects.all()
    template_name = 'my_venues.html'
    coach_settings_section = True

    def dispatch(self, request, *args, **kwargs):
        Coach.objects.get_or_create(user=request.user)
        return super(MyVenues, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MyVenues, self).get_context_data(**kwargs)
        context['venues'] = True
        return context

    def get_queryset(self):
        qs = super(MyVenues, self).get_queryset()
        return qs.filter(coach=Coach.objects.filter(user=self.request.user).first())


class CreateVenues(CreateView, FronesisBaseInnerView):
    model = Venue
    queryset = Venue.objects.all()
    template_name = 'new_venues.html'
    form_class = VenuesForm
    coach_settings_section = True

    def dispatch(self, request, *args, **kwargs):
        Coach.objects.get_or_create(user=request.user)
        return super(CreateVenues, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateVenues, self).get_context_data(**kwargs)
        context['venues'] = True
        return context

    def get_success_url(self):
        return reverse('coaches:my_venues')


class EditVenues(UpdateView, FronesisBaseInnerView):
    model = Venue
    queryset = Venue.objects.all()
    template_name = 'edit_venues.html'
    form_class = VenuesForm
    coach_settings_section = True

    def dispatch(self, request, *args, **kwargs):
        Coach.objects.get_or_create(user=request.user)
        return super(EditVenues, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EditVenues, self).get_context_data(**kwargs)
        context['venues'] = True
        return context

    def get_success_url(self):
        return reverse('coaches:my_venues')

    def get_queryset(self):
        qs = super(EditVenues, self).get_queryset()
        return qs.filter(coach=Coach.objects.filter(user=self.request.user).first())


class RemoveVenues(DeleteView, FronesisBaseInnerView):
    model = Venue
    queryset = Venue.objects.all()
    coach_settings_section = True

    def dispatch(self, request, *args, **kwargs):
        Coach.objects.get_or_create(user=request.user)
        return super(RemoveVenues, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('coaches:my_venues')

    def get_queryset(self):
        qs = super(RemoveVenues, self).get_queryset()
        return qs.filter(coach=Coach.objects.filter(user=self.request.user).first())


class MyServices(ListView, FronesisBaseInnerView):
    model = Session
    queryset = Session.objects.all()
    template_name = 'my_services.html'
    my_services_section = True

    def dispatch(self, request, *args, **kwargs):
        Coach.objects.get_or_create(user=request.user)
        return super(MyServices, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(MyServices, self).get_queryset()
        return qs.filter(coach=Coach.objects.filter(user=self.request.user).first())


class CreateService(CreateView, FronesisBaseInnerView):
    model = Session
    queryset = Session.objects.all()
    template_name = 'new_service.html'
    form_class = SessionForm
    my_services_section = True

    def dispatch(self, request, *args, **kwargs):
        Coach.objects.get_or_create(user=request.user)
        return super(CreateService, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateService, self).get_context_data(**kwargs)
        context['venues'] = True
        q1 = Q(never_expires=True)
        q2 = Q(expires=True, expiration_date__gte=datetime.now())
        context['bundles'] = Bundle.objects.filter(coach__user=self.request.user)
        return context

    def get_success_url(self):
        return reverse('coaches:my_services')

    def get_queryset(self):
        qs = super(CreateService, self).get_queryset()
        return qs.filter(coach=Coach.objects.filter(user=self.request.user).first())


class EditService(UpdateView, FronesisBaseInnerView):
    model = Session
    queryset = Session.objects.all()
    template_name = 'edit_service.html'
    form_class = SessionForm
    my_services_section = True

    def dispatch(self, request, *args, **kwargs):
        Coach.objects.get_or_create(user=request.user)
        return super(EditService, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EditService, self).get_context_data(**kwargs)
        context['venues'] = True
        return context

    def get_success_url(self):
        return reverse('coaches:edit_services', kwargs={
            'pk': self.object.pk
        })

    def get_queryset(self):
        qs = super(EditService, self).get_queryset()
        return qs.filter(coach=Coach.objects.filter(user=self.request.user).first())

SERVICE_LENGTH_CHOICE = (
    ('-1', 'Select option'),
    ('0', 'Less than an hour'),
    ('1', '1 hour'),
    ('2', '2 hours'),
    ('3', '3 hours'),
    ('4', '4 hours'),
    ('5', '5 hours'),
    ('6', '6 hours'),
    ('7', 'More than 6 hours'),
)


class CommunityView(ListView, FronesisBaseInnerView):
    model = Coach
    queryset = Coach.objects.all()
    template_name = 'community.html'
    min_price_filter = 0
    max_price_filter = 10000
    face2face = False
    online = False
    length_filter = -1

    def dispatch(self, request, *args, **kwargs):
        print(request.GET)
        self.min_price_filter = request.GET.get('price-min', self.min_price_filter)
        self.max_price_filter = request.GET.get('price-max', self.max_price_filter)
        self.face2face = True if request.GET.get('face2face', '') == 'on' else False
        self.online = True if request.GET.get('online', '') == 'on' else False
        self.length_filter = request.GET.get('length_filter', self.length_filter)
        return super(CommunityView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(CommunityView, self).get_queryset()
        qs = qs.filter(services__price__range=(self.min_price_filter, self.max_price_filter))
        qs = qs.filter(services__face_to_face=self.face2face)
        qs = qs.filter(services__online=self.online)
        if self.length_filter != '-1':
            if self.length_filter == '0':
                qs = qs.filter(services__length_hours=0, services__length_minutes__gte=0)
            elif self.length_filter == '1':
                qs = qs.filter(services__length_hours=1, services__length_minutes=0)
            elif self.length_filter == '2':
                q1 = Q(services__length_hours=1, services__length_minutes__gt=0)
                q2 = Q(services__length_hours=2, services__length_minutes=0)
                qs = qs.filter(q1 | q2)
            elif self.length_filter == '3':
                q1 = Q(services__length_hours=2, services__length_minutes__gt=0)
                q2 = Q(services__length_hours=3, services__length_minutes=0)
                qs = qs.filter(q1 | q2)
            elif self.length_filter == '4':
                q1 = Q(services__length_hours=3, services__length_minutes__gt=0)
                q2 = Q(services__length_hours=4, services__length_minutes=0)
                qs = qs.filter(q1 | q2)
            elif self.length_filter == '5':
                q1 = Q(services__length_hours=4, services__length_minutes__gt=0)
                q2 = Q(services__length_hours=5, services__length_minutes=0)
                qs = qs.filter(q1 | q2)
            elif self.length_filter == '6':
                q1 = Q(services__length_hours=5, services__length_minutes__gt=0)
                q2 = Q(services__length_hours=6, services__length_minutes=0)
                qs = qs.filter(q1 | q2)
            elif self.length_filter == '7':
                q1 = Q(services__length_hours=6, services__length_minutes__gt=0)
                q2 = Q(services__length_hours__gte=7)
                qs = qs.filter(q1 | q2)
        return qs.distinct()

    def get_context_data(self, *args, **kwargs):
        context = super(CommunityView, self).get_context_data(*args, **kwargs)
        context['min_price_filter'] = self.min_price_filter
        context['max_price_filter'] = self.max_price_filter
        context['face2face'] = self.face2face
        context['online'] = self.online
        context['length_choices'] = SERVICE_LENGTH_CHOICE
        context['length_filter'] = self.length_filter
        return context


class CoachDetailView(DetailView, FronesisBaseInnerView):
    model = Coach
    queryset = Coach.objects.all()
    template_name = 'coach_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CoachDetailView, self).get_context_data(*args, **kwargs)
        return context
