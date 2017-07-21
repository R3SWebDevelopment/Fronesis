from .views import auth_return
from django.conf.urls import url

urlpatterns = [

    url(r'^oauth2callback/$', auth_return, 'auth_return'),
]

