from rest_framework import viewsets


class OnlyAlterOwnObjectsViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user
        ) if self.request.method in (
            'PUT', 'PATCH', 'DELETE'
        ) else self.queryset
