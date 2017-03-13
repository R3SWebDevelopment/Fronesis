from .views import UserViewSet, UserProfileViewSet, MyselfView
from rest_framework.routers import DefaultRouter
from django.conf.urls import url

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet)

urlpatterns = [
    url(r'^me/$', MyselfView.as_view()),
]

urlpatterns += router.urls
