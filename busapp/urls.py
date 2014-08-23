from django.conf.urls import patterns, url

from busapp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)