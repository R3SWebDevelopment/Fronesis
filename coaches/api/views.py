from rest_framework import viewsets
from .serializers import Client, Session, Venue
from .serializers import ClientSerializer, SessionSerializer, VenueSerializer
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


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        coach = user.coaches.first()
        if coach:
            qs = coach.venues.all()
        else:
            qs = self.queryset.none()
        service_id = self.request.query_params.get('service', None)
        if service_id:
            service = Session.objects.filter(id=service_id).first()
            if service:
                qs = qs if service.all_venues else service.allow_on_venues.all()
        return qs
