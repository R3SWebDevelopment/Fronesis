from rest_framework import viewsets
from .serializers import Client, Session
from .serializers import ClientSerializer, SessionSerializer
from django.db.models import Q


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        coach = user.coaches.first()
        if coach:
            qs = coach.clients.all()
        else:
            qs = self.queryset.none()
        search = self.request.query_params.get('search', None)
        if search:
            qs = qs.filter(Q(full_name__icontains=search) | Q(email__icontains=search)).distinct()
        return qs


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        coach = user.coaches.first()
        if coach:
            qs = coach.services.all()
        else:
            qs = self.queryset.none()
        return qs
