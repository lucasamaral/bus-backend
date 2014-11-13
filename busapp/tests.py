# -*- coding: utf-8 -*-

import json

from django.test import TestCase
from django.db.models import Q

from busapp.models import Point, Stop
from busapp.views import parse_results_latlon


class PointTestCase(TestCase):
    def setUp(self):
        Point.objects.create(lat=0.0, lon=0.0)
        Point.objects.create(lat=90.0, lon=0.0)

    def test_unicode_works_point(self):
        point1 = Point.objects.get(Q(lat=0.0), Q(lon=0.0))
        point2 = Point.objects.get(Q(lat=90.0), Q(lon=0.0))
        self.assertEqual(unicode(point1), 'Lat:0000.000000 Lon:0000.000000')
        self.assertEqual(unicode(point2), 'Lat:0090.000000 Lon:0000.000000')


class StopTestCase(TestCase):
    def setUp(self):
        point1 = Point.objects.create(lat=0.0, lon=0.0)
        self.address = 'Rua X, 111'
        Stop.objects.create(name='stop1', address=self.address, point=point1)

    def test_unicode_works_stop(self):
        stop = Stop.objects.get(name='stop1')
        self.assertEqual(unicode(stop), self.address)


class ParseMapsJsonCase(TestCase):
    def setUp(self):
        string = """
{
   "results": [{
      "address_components": [{
         "long_name": "Acesso Cta",
         "short_name": "Ac. Cta",
         "types": ["route"]
      }, {
         "long_name": "Vila das Acacias",
         "short_name": "Vila das Acacias",
         "types": ["neighborhood", "political"]
      }],
      "formatted_address": "Acesso Cta, 865-969 - Vila das Acacias, São José dos Campos - SP, República Federativa do Brasil",
      "types": ["street_address"]
   }]
}""".decode('latin-1')
        self.json_dic = json.loads(string)

    def test_json_reading(self):
        (route, formatted_address) = parse_results_latlon(self.json_dic)
        name = 'Acesso Cta'.decode('latin-1')
        address = 'Acesso Cta, 865-969 - Vila das Acacias, São José dos Campos - SP, República Federativa do Brasil' \
                  .decode('latin-1')
        self.assertEqual(unicode(name), route)
        self.assertEqual(unicode(address),
                         formatted_address)
