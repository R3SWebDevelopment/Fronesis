from rest_framework import routers
from .views import ClientViewSet, SessionViewSet

router = routers.SimpleRouter()
router.register(r'clients', ClientViewSet)
router.register(r'services', SessionViewSet)

urlpatterns = router.urls
