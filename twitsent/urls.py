from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.twit_sent, name='twit_sent'),
]