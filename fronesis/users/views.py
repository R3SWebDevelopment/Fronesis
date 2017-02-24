
from fronesis.utils.mixins import OnlyAlterOwnObjectsViewSet
from .serializers import UserSerializer, UserProfileSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets
from .models import UserProfile


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserProfileViewSet(OnlyAlterOwnObjectsViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def perform_create(self, serializer):
        return serializer.save(
            user=self.request.user
        )
