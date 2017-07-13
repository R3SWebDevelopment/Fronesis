from django.views.generic import DetailView, ListView, UpdateView
from .models import Coach
from .forms import CoachContactForm
from crum import get_current_user
from utils.views import FronesisBaseInnerView
from django.core.urlresolvers import reverse


class ContactDetail(UpdateView, FronesisBaseInnerView):
    model = Coach
    queryset = Coach.objects.all()
    form_class = CoachContactForm
    object = None

    def get_form(self, form_class=None):
        form_class = self.get_form_class()
        form = form_class(instance=self.get_object())
        return form

    def get_object(self, queryset=None):
        user = get_current_user()
        instance, created = Coach.objects.get_or_create(user=user)
        self.object = instance
        return instance

    def get_context_data(self, **kwargs):
        context = super(ContactDetail, self).get_context_data(**kwargs)
        context['contact'] = True
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = form_class(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('coaches:contact_information')


class BlockedHours(DetailView):
    pass


class BookingSettings(DetailView):
    pass


class MyVenues(ListView):
    pass
