from django.views.generic import TemplateView
from django.urls import reverse
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
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


class EventView(FormView):

    template_name = 'events/edit_view.html'
    form_class = EventForm
    body_class = 'bg-white'

    def dispatch(self, request, mode='create', event_uuid=None, *args, **kwargs):
        self.mode = mode
        self.event_uuid = event_uuid
        return super(EventView, self).dispatch(request=request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EventView, self).get_context_data(**kwargs)
        context['BODY_CLASS'] = self.body_class or ''
        context['mode'] = self.mode
        return context

    def get_form(self, form_class=None):
        if self.mode == 'update' and self.event_uuid is not None:
            form_class = self.get_form_class()
            event = get_object_or_404(Event, uuid=self.event_uuid)
            form = form_class(instance=event)
            return form
        return super(EventView, self).get_form(form_class)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        if self.mode == 'create':
            form = form_class(request.POST, request.FILES)
        else:
            event = get_object_or_404(Event, uuid=self.event_uuid)
            form = form_class(request.POST, request.FILES, instance=event)
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form, **kwargs)

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        event = form.save(commit=True)
        event.save()
        return super(EventView, self).form_valid(form)

    def get_success_url(self):
        if self.mode == 'create':
            return self.event.admin_url if self.event is not None else reverse('my_events_create')
        else:
            return self.event.admin_url
