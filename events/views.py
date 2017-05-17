from django.views.generic import TemplateView, ListView, DetailView
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from datetime import datetime
from .forms import EventForm
from .models import Event


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


class MyEventsView(ListView):
    template_name = 'events/my_events.html'
    body_class = 'bg-white'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super(MyEventsView, self).dispatch(request=request, **kwargs)

    def get_queryset(self):
        return Event.objects.filter(organizer=self.user)

    def get_context_data(self, **kwargs):
        context = super(MyEventsView, self).get_context_data(**kwargs)
        context['attending_by_you'] = Event.objects.none()
        context['past_events'] = Event.past.all()
        context['BODY_CLASS'] = self.body_class or ''
        return context


class CreateEventView(CreateView):

    template_name = 'events/edit_view.html'
    form_class = EventForm
    body_class = 'bg-white'

    @method_decorator(login_required)
    def dispatch(self, request, mode='create', event_uuid=None, *args, **kwargs):
        self.mode = mode
        self.event_uuid = event_uuid
        self.organizer = request.user
        return super(CreateEventView, self).dispatch(request=request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateEventView, self).get_context_data(**kwargs)
        context['BODY_CLASS'] = self.body_class or ''
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


class EventView(UpdateView):

    template_name = 'events/edit_view.html'
    model = Event
    form_class = EventForm
    body_class = 'bg-white'

    @method_decorator(login_required)
    def dispatch(self, request, mode='create', event_uuid=None, *args, **kwargs):
        self.mode = mode
        self.event_uuid = event_uuid
        self.organizer = request.user
        if self.event_uuid is not None:
            self.event = Event.objects.filter(uuid =self.event_uuid).first()
        return super(EventView, self).dispatch(request=request, **kwargs)

    def get_object(self, queryset=None):
        return Event.objects.filter(uuid=self.event_uuid).first()

    def get_context_data(self, **kwargs):
        context = super(EventView, self).get_context_data(**kwargs)
        context['BODY_CLASS'] = self.body_class or ''
        context['mode'] = self.mode
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
        return super(EventView, self).form_valid(form)


class EventsPublished(ListView):
    template_name = 'events/published.html'
    body_class = 'bg-white'

    def dispatch(self, request, *args, **kwargs):
        return super(EventsPublished, self).dispatch(request=request, **kwargs)

    def get_queryset(self):
        return Event.publishedEvent.all()

    def get_context_data(self, **kwargs):
        context = super(EventsPublished, self).get_context_data(**kwargs)
        context['past_events'] = Event.publishedPast.all()
        context['BODY_CLASS'] = self.body_class or ''
        return context


class EventDetailPublished(DetailView):

    template_name = 'events/public-view-event.html'
    body_class = 'bg-white'

    def dispatch(self, request, year, month, day, slug, event_uuid, *args, **kwargs):
        begins_date = datetime.strptime('{}/{}/{}'.format(day, month, year), '%d/%B/%Y').date()
        self.event = Event.published_all.filter(uuid=event_uuid, begins_date=begins_date, slug=slug)
        return super(EventDetailPublished, self).dispatch(request=request)

    def get_context_data(self, **kwargs):
        context = super(EventDetailPublished, self).get_context_data(**kwargs)
        context['BODY_CLASS'] = self.body_class or ''
        return context

    def get_object(self, queryset=None):
        return self.event
