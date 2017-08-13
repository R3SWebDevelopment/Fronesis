from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from .models import Appointments, Coach, Client
from .forms import AddAppointmentForm
from crum import get_current_user
from utils.views import FronesisBaseInnerView
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta
from rest_framework.authtoken.models import Token


class CalendarView(ListView, FronesisBaseInnerView):
    model = Appointments
    queryset = Appointments.objects.all()
    template_name = 'calendar_view.html'
    month = None
    year = None
    coach = None
    date = None
    appointments_section = True

    def dispatch(self, request, *args, **kwargs):
        coach, created = Coach.objects.get_or_create(user=request.user)
        if not Token.objects.filter(user=request.user).exists():
            Token.objects.create(user=request.user)
        self.coach = coach
        try:
            self.date = datetime.strptime(request.GET.get('date', None), '%d-%m-%Y').date() \
                if request.GET.get('date', None) else datetime.now().date()
        except:
            self.date = datetime.now().date()
        return super(CalendarView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CalendarView, self).get_context_data(**kwargs)
        qs = context['object_list']
        context['calendar'] = True
        context['today'] = qs.filter(starts_datetime__year=self.date.year, starts_datetime__month=self.date.month,
                                    starts_datetime__day=self.date.day)
        context['date'] = self.date
        context['week'] = self.get_week_appointments(qs)
        context['next'] = (self.date + timedelta(days=1)).strftime('%d-%m-%Y')
        context['prev'] = (self.date - timedelta(days=1)).strftime('%d-%m-%Y')
        context['token'] = self.request.user.auth_token
        return context

    def get_week_appointments(self, qs):
        today = datetime.now().date()
        if today.isoweekday() == 1:
            monday = today
        elif today.isoweekday() == 7:
            monday = today - timedelta(days=6)
        else:
            monday = today - timedelta(days=(today.isoweekday() - 1))
        dates = [monday] + [monday + timedelta(days=x) for x in range(1, 7)]
        week = []
        for index, date in enumerate(dates):
            key = date.strftime('%a %d')
            week.append({
                'day': date,
                'appointments': qs.filter(starts_datetime__year=date.year, starts_datetime__month=date.month,
                                          starts_datetime__day=date.day),
            })
        return week

    def get_queryset(self, *args, **kwargs):
        return super(CalendarView, self).get_queryset().filter(coach=self.coach)


class ClientsView(ListView, FronesisBaseInnerView):
    model = Client
    queryset = Client.objects.all()
    template_name = 'clients.html'
    month = None
    year = None
    coach = None
    appointments_section = True

    def dispatch(self, request, *args, **kwargs):
        coach, created = Coach.objects.get_or_create(user=request.user)
        self.coach = coach
        return super(ClientsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ClientsView, self).get_context_data(**kwargs)
        context['clients'] = True
        return context

    def get_queryset(self, *args, **kwargs):
        return self.coach.clients.all()


class HistoryView(ListView, FronesisBaseInnerView):
    model = Appointments
    queryset = Appointments.objects.all()
    template_name = 'history.html'
    month = None
    year = None
    coach = None
    appointments_section = True

    def dispatch(self, request, *args, **kwargs):
        coach, created = Coach.objects.get_or_create(user=request.user)
        self.coach = coach
        return super(HistoryView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        return super(HistoryView, self).get_queryset().filter(coach=self.coach)

    def get_context_data(self, *args, **kwargs):
        now = datetime.now()
        context = super(HistoryView, self).get_context_data(*args, **kwargs)
        context['history'] = True
        qs = context['object_list']
        context['past'] = qs.filter(ends_datetime__lte=now)
        context['upcoming'] = qs.filter(starts_datetime__gte=now)
        return context


class BundleView(ListView, FronesisBaseInnerView):
    model = Client
    queryset = Client.objects.all()
    template_name = 'clients.html'
    month = None
    year = None
    coach = None
    appointments_section = True

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
    template_name = 'add.html'
    form_class = AddAppointmentForm
    appointments_section = True

