from .views import philios_web
from django.conf.urls import url

urlpatterns = [
    url(r'^$', philios_web, name='web'),
    url(r'.*$', philios_web, {'display_header': False}),
]

