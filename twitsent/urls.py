from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.twit_sent, name='twit_sent'),
    url(r'^twit_sent.html$', views.twit_sent, name='twit_sent'),
    url(r'^search', views.search, name='search')
]