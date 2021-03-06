from django.conf.urls import patterns, url, include
from rest_framework import routers

from busapp import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'points', views.PointViewSet)
router.register(r'stops', views.StopViewSet)
router.register(r'segments', views.LineSegmentViewSet)
router.register(r'buslines', views.BusLineViewSet)
router.register(r'relations', views.BusLineRelationViewSet)
router.register(r'times', views.TimeMeasuredViewSet)
router.register(r'bus', views.BusViewSet)

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^', include(router.urls)),
    url(r'^createsegment/$', views.BuildLineSegment.as_view()),
    url(r'^createmeasures/$', views.TimeMeasuredMultiViewSet.as_view()),
)
