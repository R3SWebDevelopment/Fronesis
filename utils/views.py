from django.utils.translation import activate
from django.views.generic.base import ContextMixin
from django.views import View


class EnglishView(View):

    def dispatch(self, request, *args, **kwargs):
        activate('en')
        return super(EnglishView, self).dispatch(request, **kwargs)


class FronesisBaseInnerView(ContextMixin, EnglishView):
    body_class = 'bg-white'

    def get_context_data(self, **kwargs):
        context = super(FronesisBaseInnerView, self).get_context_data(**kwargs)
        context['BODY_CLASS'] = self.body_class or ''
        return context

