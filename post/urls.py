from django.conf.urls import url
from .views import getbytype, getbynovel, getcontent, search

urlpatterns = [
    url(r'^(\d+)$', getbytype),
    url(r'^chapters/(\d+)$', getbynovel),
    url(r'^showcontent/(\d+)$', getcontent),
    url(r'^search$', search),
]
