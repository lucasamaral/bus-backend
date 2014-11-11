import requests

from django.shortcuts import render
from django.contrib.auth.models import User, Group

from rest_framework import viewsets, views, status, permissions
from rest_framework.response import Response

from busapp.serializers import UserSerializer, GroupSerializer, BusLineSerializer, \
    PointSerializer, StopSerializer, TimeMeasuredSerializer, LineSegmentSerializer, \
    LinePointRelationSerializer
from busapp.models import Point, Stop, LineSegment, BusLine, BusLineRelation, TimeMeasured, Bus
from busapp.parsers import JSONLatinParser


class BuildLineSegment(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = JSONLatinParser().parse(request)
        points = build_point_list(data['points'])
        points_ser = PointSerializer(data=points, many=True)
        if points_ser.is_valid():
            points_ser.save()
            data['first_stop']['point'] = points_ser.data[0]['id']
            data['second_stop']['point'] = points_ser.data[-1]['id']

            stop1_ser = StopSerializer(data=data['first_stop'])
            if stop1_ser.is_valid():
                stop1_ser.save()
            else:
                return Response(stop1_ser.errors, status=status.HTTP_400_BAD_REQUEST)

            stop2_ser = StopSerializer(data=data['second_stop'])
            if stop2_ser.is_valid():
                stop2_ser.save()
            else:
                return Response(stop2_ser.errors, status=status.HTTP_400_BAD_REQUEST)

            line = {}
            line['first_stop'] = stop1_ser.object.id
            line['second_stop'] = stop2_ser.object.id
            line_ser = LineSegmentSerializer(data=line)
            if line_ser.is_valid():
                line_ser.save()
                line_points = build_line_points(points_ser.data, line_ser.object.id)
                line_rels_ser = LinePointRelationSerializer(data=line_points, many=True)
                if line_rels_ser.is_valid():
                    line_rels_ser.save()
                else:
                    return Response(line_rels_ser.errors, status=status.HTTP_400_BAD_REQUEST)

                time = {}
                time['time_value'] = int(data['time_measured'])
                time['line_segment'] = line_ser.object.id
                time_ser = TimeMeasuredSerializer(data=time)
                if time_ser.is_valid():
                    time_ser.save()
                    return Response(line_ser.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(time_ser.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(line_ser.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(points_ser.errors, status=status.HTTP_400_BAD_REQUEST)


def build_line_points(points, line_seg):
    relations = []
    for idx, pt in enumerate(points):
        rel = {}
        rel['line_segment'] = line_seg
        rel['point'] = pt['id']
        rel['order'] = idx
        relations.append(rel)
    return relations


def build_point_list(points):
    parsed = []
    for pt in points:
        point = {}
        point['lat'] = float(pt['lat'])
        point['lon'] = float(pt['lon'])
        parsed.append(point)
    return parsed


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PointViewSet(viewsets.ModelViewSet):
    model = Point


class StopViewSet(viewsets.ModelViewSet):
    model = Stop

    def pre_save(self, obj):
        route = ''
        address_str = ''
        url = 'http://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s' % (obj.point.lat, obj.point.lon)
        r = requests.get(url)
        if r.status_code == 200:
            (route, address_str) = parse_results_latlon(r.json())
        if not obj.name and route:
            obj.name = route
        if not obj.address and address_str:
            obj.address = address_str


def parse_results_latlon(json):
    json_results = json['results']
    address_str = ''
    stop_name = ''
    if json_results:
        result = json_results[0]
        comps = result['address_components']
        for address in comps:
            if 'b_station' in address['types'] or 'bus_station' in address['types']:
                stop_name = address['long_name']
                break
            elif 'route' in address['types']:
                stop_name = address['long_name']
                break
        address_str = result['formatted_address']
    return (stop_name, address_str)


class TimeMeasuredViewSet(viewsets.ModelViewSet):
    model = TimeMeasured


class LineSegmentViewSet(viewsets.ModelViewSet):
    model = LineSegment


class BusViewSet(viewsets.ModelViewSet):
    model = Bus


class BusLineViewSet(viewsets.ModelViewSet):
    queryset = BusLine.objects.all()
    serializer_class = BusLineSerializer


class BusLineRelationViewSet(viewsets.ModelViewSet):
    model = BusLineRelation




def index(request):
    return render(request, 'busapp/index.html', {})
