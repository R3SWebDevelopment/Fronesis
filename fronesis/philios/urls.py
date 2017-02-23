from .views import LinkViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'links', LinkViewSet)
urlpatterns = router.urls
