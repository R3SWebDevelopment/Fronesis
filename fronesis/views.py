from django.views.generic import TemplateView
from events.models import Event
from coaches.models import Coach


class Homepage(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Homepage, self).get_context_data(*args, **kwargs)
        context['events'] = Event.publishedEvent.all()[:3]
        context['coaches'] = Coach.objects.exclude(user__profile__userprofile__avatar='')[:3]
        context['coaches_avatar'] = [a.get('user__profile__userprofile__avatar')
                                     for a in Coach.objects.
                                                  exclude(user__profile__userprofile__avatar='')
                                                  .values('user__profile__userprofile__avatar')[:3]]
        return context
