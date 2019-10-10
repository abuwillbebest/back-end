from django.conf.urls import url
from .views import getbytype, getbynovel, getcontent

urlpatterns = [
    url(r'^(\d+)$', getbytype),
    url(r'^chapters/(\d+)$', getbynovel),
    url(r'^showcontent/(\d+)$', getcontent),
]
