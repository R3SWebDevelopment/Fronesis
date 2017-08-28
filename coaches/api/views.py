from rest_framework import viewsets
from .serializers import Client, Session, Venue
from .serializers import ClientSerializer, SessionSerializer, VenueSerializer
from django.db.models import Q
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from coaches.models import Coach


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

    @detail_route(methods=['get'], url_path='my_info')
    def my_info(self, request, *args, **kwargs):
        user = self.request.user
        coach_id = request.GET.get('coach', None)
        coach = None
        if coach_id:
            coach = Coach.objects.filter(pk=coach_id).first()
            print("Coach: {}".format(coach))
        if user and coach:
            client, create = Client.objects.get_or_create(email=user.email)
            if client:
                client.full_name = user.get_full_name()
                client.save()
                coach.clients.add(client)
                return Response(ClientSerializer(client).data)
        return Response({})


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
