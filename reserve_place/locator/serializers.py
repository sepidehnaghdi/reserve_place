from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import LocatorProfile
from django.contrib.auth.models import User, Group


class LocatorProfileSerializer(serializers.ModelSerializer):
    # user_id = serializers.IntegerField()
    class Meta:
        model = LocatorProfile
        fields = '__all__'
        read_only_fields = ('user', )

