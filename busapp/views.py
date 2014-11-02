from django.shortcuts import render
from django.contrib.auth.models import User, Group

from rest_framework import viewsets, views, status, permissions
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from busapp.serializers import UserSerializer, GroupSerializer, BusLineSerializer, \
    PointSerializer, StopSerializer, TimeEstimationSerializer, LineSegmentSerializer, \
    LinePointRelationSerializer
from busapp.models import Point, Stop, LineSegment, BusLine, BusLineRelation


class BuildLineSegment(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        points = build_point_list(data['points'])
        points_serializer = PointSerializer(data=points, many=True)
        if points_serializer.is_valid():
            points_serializer.save()
            data['first_stop']['point'] = points_serializer.data[0]['id']
            data['second_stop']['point'] = points_serializer.data[-1]['id']
            time = {}
            time['time_value'] = int(data['time_estimation'])
            time_ser = TimeEstimationSerializer(data=time)
            if time_ser.is_valid():
                time_ser.save()
            else:
                return Response(time_ser.errors, status=status.HTTP_400_BAD_REQUEST)

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
            line['time_estimation'] = time_ser.object.id
            line_ser = LineSegmentSerializer(data=line)
            if line_ser.is_valid():
                line_ser.save()
                line_points = build_line_points(points_serializer.data, line_ser.object.id)
                line_rels_ser = LinePointRelationSerializer(data=line_points, many=True)
                if line_rels_ser.is_valid():
                    line_rels_ser.save()
                    return Response(line_ser.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(line_rels_ser.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(line_ser.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(points_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class LineSegmentViewSet(viewsets.ModelViewSet):
    model = LineSegment


class BusLineViewSet(viewsets.ModelViewSet):
    queryset = BusLine.objects.all()
    serializer_class = BusLineSerializer


class BusLineRelationViewSet(viewsets.ModelViewSet):
    model = BusLineRelation




def index(request):
    return render(request, 'busapp/index.html', {})
