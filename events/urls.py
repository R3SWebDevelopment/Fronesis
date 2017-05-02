from .views import IndexView
from django.conf.urls import url

urlpatterns = [
    url(r'^index.html$', IndexView.as_view()),
]

