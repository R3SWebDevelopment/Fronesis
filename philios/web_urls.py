from .views import philios_web, philios_web_inner
from django.conf.urls import url

urlpatterns = [
    url(r'^$', philios_web, name='web'),
    url(r'.*$', philios_web_inner),
]

