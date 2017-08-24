from django.utils.translation import activate
from django.views.generic.base import ContextMixin
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class EnglishView(View):

    #@login_required
    def dispatch(self, request, *args, **kwargs):
        activate('en')
        return super(EnglishView, self).dispatch(request, **kwargs)


class FronesisBaseInnerView(ContextMixin, EnglishView):
    body_class = 'bg-white'
    my_services_section = False
    appointments_section = False
    coach_settings_section = False
    events_section = False
    profile_section = False

    def get_context_data(self, **kwargs):
        context = super(FronesisBaseInnerView, self).get_context_data(**kwargs)
        context['BODY_CLASS'] = self.body_class or ''
        context['my_services_section'] = self.my_services_section or False
        context['appointments_section'] = self.appointments_section or False
        context['coach_settings_section'] = self.coach_settings_section or False
        context['events_section'] = self.events_section or False
        context['profile_section'] = self.profile_section or False
        return context


class FronesisLoggedView(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(FronesisLoggedView, self).dispatch(request, **kwargs)

