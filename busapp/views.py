from django.shortcuts import render
from django.contrib.auth.models import User, Group

from busapp.serializers import UserSerializer, GroupSerializer
from rest_framework import viewsets

from busapp.models import Point, Stop

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


def index(request):
    return render(request, 'busapp/index.html', {})