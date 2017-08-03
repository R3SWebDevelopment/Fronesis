from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from .models import Appointments, Coach, Client
from .forms import AddAppointmentForm
from crum import get_current_user
from utils.views import FronesisBaseInnerView
from django.core.urlresolvers import reverse


class CalendarView(ListView, FronesisBaseInnerView):
    model = Appointments
    queryset = Appointments.objects.all()
    template_name = 'calendar_view.html'
    month = None
    year = None
    coach = None

    def dispatch(self, request, *args, **kwargs):
        coach, created = Coach.objects.get_or_create(user=request.user)
        self.coach = coach
        return super(CalendarView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CalendarView, self).get_context_data(**kwargs)
        context['calendar'] = True
        return context

    def get_queryset(self, *args, **kwargs):
        return super(CalendarView, self).get_queryset().filter(coach=self.coach)


class ClientsView(ListView, FronesisBaseInnerView):
    model = Client
    queryset = Client.objects.all()
    template_name = 'clients.html'
    month = None
    year = None
    coach = None

    def dispatch(self, request, *args, **kwargs):
        coach, created = Coach.objects.get_or_create(user=request.user)
        self.coach = coach
        return super(ClientsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ClientsView, self).get_context_data(**kwargs)
        context['clients'] = True
        return context

    def get_queryset(self, *args, **kwargs):
        return super(ClientsView, self).get_queryset()


class HistoryView(ListView, FronesisBaseInnerView):
    model = Client
    queryset = Client.objects.all()
    template_name = 'clients.html'
    month = None
    year = None
    coach = None

    def dispatch(self, request, *args, **kwargs):
        coach, created = Coach.objects.get_or_create(user=request.user)
        self.coach = coach
        return super(HistoryView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HistoryView, self).get_context_data(**kwargs)
        context['history'] = True
        return context

    def get_queryset(self, *args, **kwargs):
        return super(HistoryView, self).get_queryset()


class BundleView(ListView, FronesisBaseInnerView):
    model = Client
    queryset = Client.objects.all()
    template_name = 'clients.html'
    month = None
    year = None
    coach = None

    def dispatch(self, request, *args, **kwargs):
        coach, created = Coach.objects.get_or_create(user=request.user)
        self.coach = coach
        return super(BundleView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BundleView, self).get_context_data(**kwargs)
        context['bundles'] = True
        return context

    def get_queryset(self, *args, **kwargs):
        return super(BundleView, self).get_queryset()


class AddAppointmentView(CreateView, FronesisBaseInnerView):
    model = Appointments
    queryset = Appointments.objects.all()
    template_name = 'clients.html'
    form_class = AddAppointmentForm

