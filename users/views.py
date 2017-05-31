from .serializers import UserSerializer, UserProfileSerializer
from utils.mixins import OnlyAlterOwnObjectsViewSet
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import UserProfile
from django.views.generic import TemplateView, FormView
from utils.views import FronesisBaseInnerView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserChangeForm, SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class MyselfView(APIView):
    queryset = User.objects.all()

    def get_queryset(self):
        u = self.request.user
        q = self.queryset

        return q.filter(
            id=u.id
        ) if u.is_authenticated else q.none()

    def get(self, request, format=None):
        return Response(
            UserSerializer(self.get_queryset().first(), many=False).data
        )


class UserProfileViewSet(OnlyAlterOwnObjectsViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def perform_create(self, serializer):
        return serializer.save(
            user=self.request.user
        )


class DashboardView(TemplateView, FronesisBaseInnerView):
    template_name = 'users/dashboard.html'


class ProfileView(FormView, FronesisBaseInnerView):
    template_name = 'users/profile.html'
    model = User
    form_class = UserChangeForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super(ProfileView, self).dispatch(request,  *args, **kwargs)

    def get_object(self, queryset=None):
        return self.user

    def get_form(self, form_class=None):
        return self.form_class(instance=self.get_object())

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        data = request.POST
        form = self.form_class(instance=user, data=data)
        data['username'] = user.username
        data['date_joined'] = user.date_joined
        data['username'] = user.username
        data['is_active'] = user.is_active
        data['is_staff'] = user.is_staff
        data['is_superuser'] = user.is_superuser
        if form.is_valid():
            password = data.get('new_password1', None)
            if password is not None and password.strip():
                password_form = SetPasswordForm(user=self.get_object(), data=data)
                if password_form.is_valid():
                    user = password_form.save()
                    update_session_auth_hash(request, user)
                else:
                    return self.form_invalid(form)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data()
        context['password'] = SetPasswordForm(user=self.get_object())
        return context

    def form_valid(self, form):
        instance = form.save()
        instance.save()
        return super(ProfileView, self).form_valid(form)

    def get_success_url(self):
        return reverse('profile')
