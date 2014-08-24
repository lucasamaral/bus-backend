from django.conf.urls import patterns, url, include
from rest_framework import routers

from busapp import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'points', views.PointViewSet)
router.register(r'stops', views.StopViewSet)

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^', include(router.urls)),
)