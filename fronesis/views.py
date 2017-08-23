from django.views.generic import TemplateView
from events.models import Event


class Homepage(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Homepage, self).get_context_data(*args, **kwargs)
        context['events'] = Event.publishedEvent.all()[:3]
        return context
