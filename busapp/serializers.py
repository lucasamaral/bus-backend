from django.contrib.auth.models import User, Group
from rest_framework import serializers
from busapp.models import BusLine, Point, LineSegment, Stop, LinePointRelation, TimeMeasured


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point


class LineSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineSegment


class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop


class LinePointRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinePointRelation


class TimeMeasuredSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeMeasured


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class BusLineSerializer(serializers.ModelSerializer):
    start_segment = serializers.Field(source='get_start_segment')
    end_segment = serializers.Field(source='get_end_segment')
    stop_points = serializers.Field(source='stop_points')

    class Meta:
        model = BusLine
        fields = ('name', 'number', 'segments', 'start_segment', 'end_segment', 'stop_points')
