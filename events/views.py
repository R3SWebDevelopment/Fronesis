from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.http import Http404
from datetime import datetime
from .forms import EventForm, EventGetTicketForm, TicketSelectionFormSet
from .models import Event, ShoppingCart, TicketSelection, Ticket, TicketSalesOrder
from utils.utils import get_logged_user
from utils.views import FronesisBaseInnerView


class DummyView(TemplateView):

    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        self.template_name = kwargs.get('template_name', "index.html")
        self.body_class = kwargs.get('body_class', None)
        return super(DummyView, self).dispatch(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DummyView, self).get_context_data(**kwargs)
        context['BODY_CLASS'] = self.body_class or ''
        return context


class MyEventsView(ListView, FronesisBaseInnerView):
    template_name = 'events/my_events.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = get_logged_user(request)
        return super(MyEventsView, self).dispatch(request=request, **kwargs)

    def get_queryset(self):
        return Event.objects.filter(organizer=self.user)

    def get_context_data(self, **kwargs):
        context = super(MyEventsView, self).get_context_data(**kwargs)
        context['attending_by_you'] = Event.objects.none()
        context['past_events'] = Event.past.all()
        return context


class CreateEventView(CreateView, FronesisBaseInnerView):

    template_name = 'events/edit_view.html'
    form_class = EventForm

    @method_decorator(login_required)
    def dispatch(self, request, mode='create', event_uuid=None, *args, **kwargs):
        self.mode = mode
        self.event_uuid = event_uuid
        self.organizer = get_logged_user(request)
        return super(CreateEventView, self).dispatch(request=request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateEventView, self).get_context_data(**kwargs)
        context['mode'] = self.mode
        return context

    def get_form(self, form_class=None):
        if self.mode == 'update' and self.event_uuid is not None:
            form_class = self.get_form_class()
            event = get_object_or_404(Event, uuid=self.event_uuid)
            form = form_class(instance=event)
            return form
        return super(CreateEventView, self).get_form(form_class)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        if self.mode == 'create':
            form = form_class(request.POST, request.FILES)
        else:
            event = get_object_or_404(Event, uuid=self.event_uuid)
            form = form_class(request.POST, request.FILES, instance=event)
            valid = form.is_valid()
            self.post_data = request.POST
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form, **kwargs)

    def form_valid(self, form):
        self.event = form.save(commit=False)
        if self.mode == 'create':
            self.event.organizer = self.organizer
        self.event.save()
        if self.mode == 'update':
            current_tickets = []
            ids = self.post_data.getlist('ticket[]') or []
            names = self.post_data.getlist('name[]') or []
            prices = self.post_data.getlist('price[]') or []
            totals = self.post_data.getlist('total[]') or []
            tickets_data = zip(ids, names, prices, totals)
            for ticket_data in tickets_data:
                ticket = self.event.define_ticket_type(*ticket_data)
                current_tickets.append(ticket)
            self.event.clean_tickets(exclude=current_tickets)
        return super(CreateEventView, self).form_valid(form)

    def get_success_url(self):
        if self.mode == 'create':
            return self.event.admin_url if self.event is not None else reverse('my_events_create')
        else:
            return self.event.admin_url


class EventView(UpdateView, FronesisBaseInnerView):

    template_name = 'events/edit_view.html'
    model = Event
    form_class = EventForm

    @method_decorator(login_required)
    def dispatch(self, request, mode='create', event_uuid=None, *args, **kwargs):
        self.mode = mode
        self.event_uuid = event_uuid
        self.organizer = get_logged_user(request)
        if self.event_uuid is not None:
            self.event = Event.objects.filter(uuid=self.event_uuid).filter(organizer=self.organizer).first()
        return super(EventView, self).dispatch(request=request, **kwargs)

    def get_object(self, queryset=None):
        return Event.objects.filter(uuid=self.event_uuid).first()

    def get_context_data(self, **kwargs):
        context = super(EventView, self).get_context_data(**kwargs)
        context['mode'] = self.mode
        context['event'] = self.event
        return context

    def get_success_url(self):
        if self.mode == 'create':
            return self.event.admin_url if self.event is not None else reverse('my_events_create')
        else:
            return self.event.admin_url

    def post(self, request, *args, **kwargs):
        self.post_data = request.POST
        return super(EventView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        self.event = form.save(commit=False)
        # if self.mode == 'create':
            # self.event.organizer = self.organizer
        self.event.organizer = self.organizer
        self.event.save()
        if self.mode == 'update':
            current_tickets = []
            ids = self.post_data.getlist('ticket[]') or []
            names = self.post_data.getlist('name[]') or []
            prices = self.post_data.getlist('price[]') or []
            totals = self.post_data.getlist('total[]') or []
            tickets_data = zip(ids, names, prices, totals)
            for ticket_data in tickets_data:
                ticket = self.event.define_ticket_type(*ticket_data)
                current_tickets.append(ticket)
            self.event.clean_tickets(exclude=current_tickets)
        return super(EventView, self).form_valid(form)


class EventTicketSalesReport(ListView, FronesisBaseInnerView):
    template_name = 'events/ticket_sales_report.html'
    model = Ticket

    @method_decorator(login_required)
    def dispatch(self, request, event_uuid, *args, **kwargs):
        self.uuid = event_uuid
        self.instance = Event.objects.get(uuid=self.uuid)
        return super(EventTicketSalesReport, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super(EventTicketSalesReport, self).get_queryset().filter(event=self.instance)

    def get_sales_order(self):
        return self.instance.sales_order

    def get_context_data(self, **kwargs):
        context = super(EventTicketSalesReport, self).get_context_data(**kwargs)
        context['event'] = self.instance
        context['sales_order'] = self.get_sales_order()
        return context


class EventsPublished(ListView, FronesisBaseInnerView):
    template_name = 'events/published.html'

    def dispatch(self, request, *args, **kwargs):
        return super(EventsPublished, self).dispatch(request=request, **kwargs)

    def get_queryset(self):
        return Event.publishedEvent.all()

    def get_context_data(self, **kwargs):
        context = super(EventsPublished, self).get_context_data(**kwargs)
        context['past_events'] = Event.publishedPast.all()
        return context


class EventDetailPublished(DetailView, FronesisBaseInnerView):

    template_name = 'events/public-view-event.html'

    def dispatch(self, request, year, month, day, slug, event_uuid, *args, **kwargs):
        begins_date = datetime.strptime('{}/{}/{}'.format(day, month, year), '%d/%B/%Y').date()
        self.event = Event.published_all.filter(uuid=event_uuid, begins_date=begins_date, slug=slug).first()
        if self.event is None:
            raise Http404
        return super(EventDetailPublished, self).dispatch(request=request)

    def get_context_data(self, **kwargs):
        context = super(EventDetailPublished, self).get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        return self.event


class EventGetTicket(FormView, FronesisBaseInnerView):
    template_name = 'events/get-tickets.html'
    form_class = TicketSelectionFormSet
    no_tickets_selected = False

    def dispatch(self, request, year, month, day, slug, event_uuid, *args, **kwargs):
        self.request = request
        begins_date = datetime.strptime('{}/{}/{}'.format(day, month, year), '%d/%B/%Y').date()
        self.event = Event.published_all.filter(uuid=event_uuid, begins_date=begins_date, slug=slug).first()
        self.user = get_logged_user(request)
        if self.event is None:
            raise Http404
        return super(EventGetTicket, self).dispatch(request=request)

    def get(self, request, *args, **kwargs):
        cart_id = self.request.session.get('ticket_cart_id', None)
        buyer = self.user if self.user is not None and self.user.is_authenticated else None
        try:
            self.cart = ShoppingCart.objects.get(id=cart_id, event=self.event, buyer=buyer)
        except ShoppingCart.DoesNotExist:
            self.cart = ShoppingCart.objects.create(event=self.event, buyer=buyer)
        self.cart.update_event_tickets()
        self.request.session['ticket_cart_id'] = self.cart.id
        self.ticket_selection = TicketSelectionFormSet(queryset=TicketSelection.objects.filter(cart=self.cart))
        return super(EventGetTicket, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        cart_id = self.request.session.get('ticket_cart_id', None)
        buyer = self.user if self.user is not None and self.user.is_authenticated else None
        try:
            self.cart = ShoppingCart.objects.get(id=cart_id, event=self.event, buyer=buyer)
        except ShoppingCart.DoesNotExist:
            pass
        self.ticket_selection = TicketSelectionFormSet(request.POST,
                                                       queryset=TicketSelection.objects.filter(cart=self.cart))
        if self.ticket_selection.is_valid():
            total_ticket_selected = 0
            for ticket in self.ticket_selection.cleaned_data:
                total_ticket_selected += ticket.get('qty', 0)
            if total_ticket_selected > 0:
                self.ticket_selection.save()
                return self.form_valid(self.ticket_selection, **kwargs)
            else:
                self.no_tickets_selected = True
                self.ticket_selection = TicketSelectionFormSet(queryset=TicketSelection.objects.filter(cart=self.cart))
                return self.form_invalid(self.ticket_selection, **kwargs)
        else:
            return self.form_invalid(self.ticket_selection, **kwargs)

    def get_success_url(self):
        return self.event.get_tickets_checkout_url

    def get_context_data(self, **kwargs):
        context = super(EventGetTicket, self).get_context_data(**kwargs)
        context['form'] = self.ticket_selection
        context['object'] = self.event
        context['user'] = self.user
        context['no_tickets_selected'] = self.no_tickets_selected
        return context


class EventGetTicketCheckOut(FormView, FronesisBaseInnerView):
    template_name = 'events/get-tickets-checkout.html'
    form_class = TicketSelectionFormSet
    no_tickets_selected = False
    error_message = []
    ticket_selection = None

    def dispatch(self, request, year, month, day, slug, event_uuid, *args, **kwargs):
        self.request = request
        begins_date = datetime.strptime('{}/{}/{}'.format(day, month, year), '%d/%B/%Y').date()
        self.event = Event.published_all.filter(uuid=event_uuid, begins_date=begins_date, slug=slug).first()
        self.user = get_logged_user(request)
        buyer = self.user if self.user is not None and self.user.is_authenticated else None
        if self.event is None:
            raise Http404
        cart_id = self.request.session.get('ticket_cart_id', None)
        try:
            self.cart = ShoppingCart.objects.get(id=cart_id, event=self.event, buyer=buyer)
        except ShoppingCart.DoesNotExist:
            raise Http404
        return super(EventGetTicketCheckOut, self).dispatch(request=request)

    def get(self, request, *args, **kwargs):
        self.ticket_selection = TicketSelectionFormSet(queryset=TicketSelection.objects.filter(cart=self.cart).
                                                       filter(selected=True))
        self.form = EventGetTicketForm(instance=self.cart)
        return super(EventGetTicketCheckOut, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.ticket_selection = TicketSelectionFormSet(queryset=TicketSelection.objects.filter(cart=self.cart).
                                                       filter(selected=True))
        self.form = EventGetTicketForm(request.POST, instance=self.cart)
        if self.form.is_valid():
            valid = True
            clean_data = self.form.cleaned_data
            if len(clean_data.get('credit_card_number')) != 16:
                self.error_message.append('Wrong Credit Card number')
                valid = False
            elif not clean_data.get('credit_card_number').isdigit():
                self.error_message.append('Wrong Credit Card number')
                valid = False
            try:
                expiration_date = datetime.strptime('01/{}/{}'.format(clean_data.get('credit_card_exp_month'),
                                                                      clean_data.get('credit_card_exp_year')),
                                                    '%d/%m/%Y')
                if expiration_date == datetime.now():
                    valid = False
                    self.error_message.append('Wrong expiration date')
            except ValueError:
                valid = False
                self.error_message.append('Wrong expiration date')
            if valid:
                return self.form_valid(self.form, **kwargs)
            else:
                return self.form_invalid(self.form, **kwargs)
        else:
            return self.form_invalid(self.form, **kwargs)

    def form_valid(self, form):
        self.cart = self.form.save()
        clean_data = self.form.cleaned_data
        cc_number = clean_data.get('credit_card_number')
        cc_exp_month = clean_data.get('credit_card_exp_month')
        cc_exp_year = clean_data.get('credit_card_exp_year')
        cc_cvv = clean_data.get('credit_card_cvv')
        self.cart.process_payment(cc_number=cc_number, cc_exp_month=cc_exp_month, cc_exp_year=cc_exp_year,
                                  cc_cvv=cc_cvv)
        return super(EventGetTicketCheckOut, self).form_valid(form)

    def get_success_url(self):
        return self.event.get_tickets_checkout_finished_url

    def get_context_data(self, **kwargs):
        context = super(EventGetTicketCheckOut, self).get_context_data(**kwargs)
        context['form'] = self.ticket_selection
        context['car_form'] = self.form
        context['object'] = self.event
        context['user'] = self.user
        context['cart'] = self.cart
        context['no_tickets_selected'] = self.no_tickets_selected
        context['error_message'] = self.error_message
        return context


class EventGetTicketCheckOutFinished(FormView, FronesisBaseInnerView):
    template_name = 'events/get-tickets-checkout_finish.html'
    form_class = TicketSelectionFormSet

    def dispatch(self, request, year, month, day, slug, event_uuid, *args, **kwargs):
        self.request = request
        begins_date = datetime.strptime('{}/{}/{}'.format(day, month, year), '%d/%B/%Y').date()
        self.event = Event.published_all.filter(uuid=event_uuid, begins_date=begins_date, slug=slug).first()
        self.user = get_logged_user(request)
        buyer = self.user if self.user is not None and self.user.is_authenticated else None
        if self.event is None:
            raise Http404
        cart_id = self.request.session.get('ticket_cart_id', None)
        # try:
        #     self.cart = ShoppingCart.objects.get(id=cart_id, event=self.event, buyer=buyer)
        # except ShoppingCart.DoesNotExist:
        #     raise Http404
        del self.request.session['ticket_cart_id']
        return super(EventGetTicketCheckOutFinished, self).dispatch(request=request)

    def get(self, request, *args, **kwargs):
        # self.ticket_selection = TicketSelectionFormSet(queryset=TicketSelection.objects.filter(cart=self.cart).
        #                                                filter(selected=True))
        # self.form = EventGetTicketForm(instance=self.cart)
        return super(EventGetTicketCheckOutFinished, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EventGetTicketCheckOutFinished, self).get_context_data(**kwargs)
        # context['form'] = self.ticket_selection
        # context['car_form'] = self.form
        context['object'] = self.event
        # context['user'] = self.user
        # context['cart'] = self.cart
        return context
