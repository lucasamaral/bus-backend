from django.contrib.auth.models import User, Group
from rest_framework import serializers
from busapp.models import BusLine


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

    class Meta:
        model = BusLine
        fields = ('name', 'number', 'segments', 'start_segment', 'end_segment')
