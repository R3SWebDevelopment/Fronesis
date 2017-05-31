from .views import UserViewSet, UserProfileViewSet, MyselfView, DashboardView, ProfileView
from rest_framework.routers import DefaultRouter
from django.conf.urls import url

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet)

urlpatterns = [
    url(r'^me/$', MyselfView.as_view()),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
]

urlpatterns += router.urls
