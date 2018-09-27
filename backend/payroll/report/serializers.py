from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import PayrollFile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class PayrollFileSerializer(serializers.ModelSerializer):

    class Meta():
        model = PayrollFile
        fields = ('file', 'id', 'timestamp')
