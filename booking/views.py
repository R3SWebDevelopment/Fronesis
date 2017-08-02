from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from .models import Appointments, Coach
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

