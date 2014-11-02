from django.shortcuts import render
from django.contrib.auth.models import User, Group

from rest_framework import viewsets, views, status, permissions
from rest_framework.response import Response

from busapp.serializers import UserSerializer, GroupSerializer, BusLineSerializer, \
    PointSerializer
from busapp.models import Point, Stop, LineSegment, BusLine, BusLineRelation


class BuildLineSegment(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        points = build_point_list(request.DATA['points'])
        print points
        serializer = PointSerializer(data=points, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def build_point_list(points):
    parsed = []
    for pt in points:
        splited = pt.split(',')
        point = {}
        point['lat'] = float(splited[0])
        point['lon'] = float(splited[1])
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
