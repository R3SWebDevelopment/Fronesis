from rest_framework import viewsets
from .serializers import Coach
from .serializers import AvailableTimeSerializer


class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Coach.objects.all()
    serializer_class = AvailableTimeSerializer

    def get_queryset(self, *args, **kwargs):
        qs = super(CalendarViewSet, self).get_queryset(*args, **kwargs)
        return qs.filter(user=self.request.user)

    def get_object(self, *args, **kwargs):
        return self.get_queryset(*args, **kwargs).first()

