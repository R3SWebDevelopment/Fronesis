from .serializers import UserSerializer, UserProfileSerializer
from utils.mixins import OnlyAlterOwnObjectsViewSet
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import UserProfile
from django.views.generic import TemplateView
from utils.views import FronesisBaseInnerView


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
