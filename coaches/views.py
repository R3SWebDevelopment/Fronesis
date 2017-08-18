from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from .models import Coach, Venue, Session
from .forms import CoachContactForm, CoachBlockedHours, CoachBookingSettings, VenuesForm, SessionForm
from crum import get_current_user
from utils.views import FronesisBaseInnerView
from django.core.urlresolvers import reverse


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


class CommunityView(ListView, FronesisBaseInnerView):
    model = Coach
    queryset = Coach.objects.all()
    template_name = 'community.html'

    def dispatch(self, request, *args, **kwargs):
        return super(CommunityView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(CommunityView, self).get_queryset()
        return qs
