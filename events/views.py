from django.views.generic import TemplateView


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
