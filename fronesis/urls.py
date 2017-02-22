from rest_framework_swagger.views import get_swagger_view
from django.conf.urls import url, include
from django.contrib import admin


admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^docs/', get_swagger_view()),

    url("^", include("drum.links.urls")),
    url("^", include("mezzanine.urls")),
]

handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
