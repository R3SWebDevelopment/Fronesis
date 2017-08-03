from rest_framework import routers
from .views import CalendarViewSet

router = routers.SimpleRouter()
router.register(r'calendar', CalendarViewSet)

urlpatterns = router.urls
