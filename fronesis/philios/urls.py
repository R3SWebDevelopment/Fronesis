from .views import LinkViewSet, RatingViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'links', LinkViewSet)
router.register(r'ratings', RatingViewSet)
urlpatterns = router.urls
