from rest_framework import routers
from .views import CalendarViewSet, AppointmentViewSet

router = routers.SimpleRouter()
router.register(r'calendar', CalendarViewSet)
router.register(r'appointment', AppointmentViewSet)

urlpatterns = router.urls
