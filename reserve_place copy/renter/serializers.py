from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User, Group
from .models import RenterProfile

class RenterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RenterProfile
        fields = '__all__'
        read_only_fields = ('user', )

