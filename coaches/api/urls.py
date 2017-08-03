from rest_framework import routers
from .views import ClientViewSet

router = routers.SimpleRouter()
router.register(r'clients', ClientViewSet)

urlpatterns = router.urls
