from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from .models import Coach, Venue, Session
from .forms import CoachContactForm, CoachBlockedHours, CoachBookingSettings, VenuesForm
from crum import get_current_user
from utils.views import FronesisBaseInnerView
from django.core.urlresolvers import reverse


class ContactDetail(UpdateView, FronesisBaseInnerView):
    model = Coach
    queryset = Coach.objects.all()
    form_class = CoachContactForm
    object = None
    template_name = 'detail.html'

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

    def get_context_data(self, **kwargs):
        context = super(EditVenues, self).get_context_data(**kwargs)
        context['venues'] = True
        return context

    def get_success_url(self):
        return reverse('coaches:edit_venues', kwargs={
            'pk': self.object.pk
        })

    def get_queryset(self):
        qs = super(EditVenues, self).get_queryset()
        return qs.filter(coach=Coach.objects.filter(user=self.request.user).first())


class RemoveVenues(DeleteView, FronesisBaseInnerView):
    model = Venue
    queryset = Venue.objects.all()

    def get_success_url(self):
        return reverse('coaches:my_venues')

    def get_queryset(self):
        qs = super(RemoveVenues, self).get_queryset()
        return qs.filter(coach=Coach.objects.filter(user=self.request.user).first())


class MyServices(ListView, FronesisBaseInnerView):
    model = Session
    queryset = Session.objects.all()
    template_name = 'my_services.html'

    def get_queryset(self):
        qs = super(MyServices, self).get_queryset()
        return qs.filter(coach=Coach.objects.filter(user=self.request.user).first())


class CreateService(CreateView, FronesisBaseInnerView):
    model = Session
    queryset = Session.objects.all()
    template_name = 'new_service.html'
    form_class = VenuesForm

    def get_context_data(self, **kwargs):
        context = super(CreateService, self).get_context_data(**kwargs)
        context['venues'] = True
        return context

    def get_success_url(self):
        return reverse('coaches:my_venues')

    def get_queryset(self):
        qs = super(CreateService, self).get_queryset()
        return qs.filter(coach=Coach.objects.filter(user=self.request.user).first())
