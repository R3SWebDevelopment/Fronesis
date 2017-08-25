from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from .models import Appointments, Coach, Client, AppointmentRequest, Session, ServicePayment
from .forms import AddAppointmentForm, AppointmentRequestConfirmForm, CreditCardForm
from crum import get_current_user
from utils.views import FronesisBaseInnerView
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class CalendarView(ListView, FronesisBaseInnerView):
    model = Appointments
    queryset = Appointments.objects.all()
    template_name = 'calendar_view.html'
    month = None
    year = None
    coach = None
    date = None
    appointments_section = True

    @method_decorator(login_required)
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
                                    starts_datetime__day=self.date.day).order_by('starts_datetime')
        context['date'] = self.date
        context['week'] = self.get_week_appointments(qs)
        context['next'] = (self.date + timedelta(days=1)).strftime('%d-%m-%Y')
        context['prev'] = (self.date - timedelta(days=1)).strftime('%d-%m-%Y')
        context['token'] = self.request.user.auth_token
        return context

    def get_week_appointments(self, qs):
        today = self.date
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
                                          starts_datetime__day=date.day).order_by('starts_datetime'),
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

    @method_decorator(login_required)
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

    @method_decorator(login_required)
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

    @method_decorator(login_required)
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

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AddAppointmentView, self).dispatch(request, *args, **kwargs)


class AppointmentRequestView(ListView, FronesisBaseInnerView):
    model = AppointmentRequest
    queryset = AppointmentRequest.objects.all()
    template_name = 'confirmation.html'
    appointments_section = True

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AppointmentRequestView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super(AppointmentRequestView, self).get_queryset()
        user = self.request.user
        return qs.filter(service__coach__user__pk=user.pk).order_by('starts_datetime')

    def get_context_data(self, **kwargs):
        context = super(AppointmentRequestView, self).get_context_data(**kwargs)
        context['confirmation'] = True
        context['form'] = AppointmentRequestConfirmForm()
        return context


class AppointmentRequestRemoveView(DeleteView, FronesisBaseInnerView):
    model = AppointmentRequest
    queryset = AppointmentRequest.objects.all()
    template_name = 'confirmation.html'
    appointments_section = True

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AppointmentRequestRemoveView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return reverse('booking:confirmation')


class AppointmentRequestConfirmView(UpdateView, FronesisBaseInnerView):
    model = AppointmentRequest
    queryset = AppointmentRequest.objects.all()
    template_name = 'confirmation.html'
    appointments_section = True
    form_class = AppointmentRequestConfirmForm
    appointment_id = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AppointmentRequestConfirmView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        if self.appointment_id:
            return reverse('google:add_appointment', kwargs={
                'pk': self.appointment_id
            })
        else:
            return reverse('booking:calendar_view')

    def get_form(self, *args, **kwargs):
        return self.get_form_class()(self.request.POST, instance=self.get_object())

    def post(self, *args, **kwargs):
        form = self.get_form(*args, **kwargs)
        if form.is_valid():
            appointment = form.save()
            if appointment.coach.google_calendar_account_id:
                self.appointment_id = appointment.pk
            instance = self.get_object()
            instance.delete()
            return self.form_valid(form)


class AppointmentClientSideModalView(DetailView, FronesisBaseInnerView):
    model = Session
    queryset = Session.objects.all()
    template_name = 'client_side_appointment_modal.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AppointmentClientSideModalView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(AppointmentClientSideModalView, self).get_context_data(*args, **kwargs)
        user = self.request.user
        token = user.auth_token
        session = self.get_object()
        coach = session.coach.pk
        service = session.pk
        context['token'] = token
        context['coach'] = coach
        context['service'] = service
        context['url'] = reverse('coaches:community')
        return context


class MyAppointmentsView(ListView, FronesisBaseInnerView):
    model = Appointments
    queryset = Appointments.objects.all()
    template_name = 'my_appointments.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MyAppointmentsView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super(MyAppointmentsView, self).get_queryset(*args, **kwargs)

        qs = qs.filter(client__email__iexact=self.request.user.email)

        return qs.order_by('starts_datetime').distinct()

    def get_context_data(self, *args, **kwargs):
        context = super(MyAppointmentsView, self).get_context_data(*args, **kwargs)
        qs = context['object_list']
        now = datetime.now()
        context['my_appointments'] = True
        context['last_appointments'] = qs.filter(starts_datetime__lte = now)
        context['object_list'] = qs.filter(starts_datetime__gte = now)
        return context


class PayAppointmentView(DetailView, FronesisBaseInnerView):
    model = Appointments
    queryset = Appointments.objects.all()
    template_name = 'pay_appointments.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        response = super(PayAppointmentView, self).dispatch(request, *args, **kwargs)
        instance = self.get_object()
        url = reverse('booking:pay_appointment_by_cc', kwargs={
            'pk': instance.pk
        })
        return redirect(url)
        #return super(PayAppointmentView, self).dispatch(request, *args, **kwargs)


class PayAppointmentByCreditCardView(UpdateView, FronesisBaseInnerView):
    model = ServicePayment
    queryset = ServicePayment.objects.all()
    template_name = 'appointment_pay_cc_form.html'
    form_class = CreditCardForm

    @method_decorator(login_required)
    def dispatch(self, request, pk, *args, **kwargs):
        appointment = Appointments.objects.filter(pk=pk).first()
        payment_info = appointment.payment_info
        if payment_info is None:
            payment_info = appointment.generate_payment_info()
        if payment_info:
            pk = payment_info.pk
        self.pk = pk
        return super(PayAppointmentByCreditCardView, self).dispatch(request=request, pk=pk, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        qs = self.get_queryset()
        return qs.filter(pk=self.pk).first()

    def get_form(self):
        instance = self.get_object()
        user =self.request.user
        first_name= user.first_name
        last_name = user.last_name
        email = user.email
        amount = instance.amount
        order = instance.pk
        description = instance.description
        return self.form_class(initial={
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'amount': amount,
            'order': order,
            'description': description,
        })
