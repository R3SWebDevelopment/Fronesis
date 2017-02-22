from rest_framework_swagger.views import get_swagger_view
from django.conf.urls import url, include
from .admin import admin_site

urlpatterns = [
    url(r'^admin/', include(admin_site.urls)),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^docs/', get_swagger_view()),

    url(r'^api/', include('fronesis.philios.urls')),
]
