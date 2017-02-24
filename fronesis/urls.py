from rest_framework_swagger.views import get_swagger_view
from django.conf.urls import url, include
from .admin import admin_site

urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'^philios/', include('fronesis.philios.urls')),

    url(r'^admin/', include(admin_site.urls)),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^docs/', get_swagger_view()),
    url("^", include("drum.links.urls")),
    url("^", include("mezzanine.urls"))
]
