from rest_framework_swagger.views import get_swagger_view
from django.conf.urls import url, include
from .admin import admin_site

urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'^philios/', include('philios.urls')),
    url(r'^philios-web/', include('philios.web_urls', namespace='philios')),
    url(r'^users/', include('users.urls')),

    url(r'^admin/', include(admin_site.urls)),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^docs/', get_swagger_view()),

    url(r'^events/', include('events.urls')),
    url(r'^coach/', include('coaches.urls', namespace='coaches')),
    url(r'^booking/', include('booking.urls', namespace='booking')),
    url(r'^google/', include('google_api.urls', namespace='google')),

    url("^", include("drum.links.urls")),
    url("^", include("mezzanine.urls")),
    url(r'^api/', include('coaches.api.urls')),
    url(r'^api/', include('booking.api.urls')),
]
