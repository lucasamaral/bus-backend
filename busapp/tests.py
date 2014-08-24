from django.test import TestCase
from django.db.models import Q

from busapp.models import Point, Stop

class PointTestCase(TestCase):
    def setUp(self):
        Point.objects.create(lat=0.0, lon=0.0)
        Point.objects.create(lat=90.0, lon=0.0)

    def test_unicode_works_point(self):
        point1 = Point.objects.get(Q(lat=0.0), Q(lon=0.0))
        point2 = Point.objects.get(Q(lat=90.0), Q(lon=0.0))
        self.assertEqual(unicode(point1), 'Lat:000.000000Lon:000.000000')
        self.assertEqual(unicode(point2), 'Lat:090.000000Lon:000.000000')

class StopTestCase(TestCase):
    def setUp(self):
        point1 = Point.objects.create(lat=0.0, lon=0.0)
        self.address = 'Rua X, 111'
        Stop.objects.create(name='stop1', address=self.address, point=point1)
    
    def test_unicode_works_stop(self):
        stop = Stop.objects.get(name='stop1')
        self.assertEqual(unicode(stop), self.address)
