from rest_framework import routers
from .views import ClientViewSet, SessionViewSet, VenueViewSet

router = routers.SimpleRouter()
router.register(r'clients', ClientViewSet)
router.register(r'services', SessionViewSet)
router.register(r'venues', VenueViewSet)

urlpatterns = router.urls
