from django.contrib.auth.models import User, Group
from rest_framework import serializers, response
from rest_framework.validators import UniqueValidator
from django.db import transaction
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, \
    HTTP_400_BAD_REQUEST
from json import loads, dumps
from utils.views import generate_confirmation_key, send_confirmation_email
from .models import EmailConfirmation
import datetime
from django.contrib.auth.hashers import make_password
from locator.models import LocatorProfile
from renter.models import RenterProfile


class DjangoGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class GroupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=80)

    class Meta:
        model = Group
        fields = ('name',)

    def validate_name(self, value):
        try:
            Group.objects.get(name=value)
        except:
            raise serializers.ValidationError("Invalid Group")

        return value


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    groups = GroupSerializer(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'groups')
        write_only_fields = ('password', 'first_name', 'last_name', 'groups', 'email')
        read_only_fields = ('id',)

    def create(self, validated_data):
        from django.contrib.auth.hashers import make_password
        with transaction.atomic():
            user = User.objects.create(
                email=validated_data.get('email'),
                first_name=validated_data.get('first_name'),
                last_name=validated_data.get('last_name'),
                username=validated_data.get('username'),
                password=make_password(validated_data.get('password')),
                is_active=False
            )
            try:
                group_dict = self.validated_data.get('groups', {'name': 'renter'})
                group = Group.objects.get(name=group_dict['name'])
                user.groups.add(group)

                if group_dict['name'] == 'locator':
                    LocatorProfile.objects.create(user=user)
                elif group_dict['name'] == 'renter':
                    RenterProfile.objects.create(user=user)

            except Group.DoesNotExist:
                group = Group.objects.get(name='renter')
                user.groups.add(group)

            # send email for confirmation
            try:
                confirmation_key = generate_confirmation_key(validated_data.get('email'))
                EmailConfirmation.objects.create(
                    user=user,
                    confirmation_key=confirmation_key,
                    expire_time=datetime.datetime.now() + datetime.timedelta(hours=24)
                )
                send_confirmation_email(validated_data.get('email'), confirmation_key)
            except Exception as e:
                print(str(e))
                raise HTTP_400_BAD_REQUEST

        return user


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'groups')
        write_only_fields = ('password', 'first_name', 'last_name', 'email')
        read_only_fields = ('id', 'username', 'groups')

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        # instance.username = instance.username
        instance.password = make_password(validated_data.get('password', instance.password))

        # new_groups = validated_data.get('groups', None)
        # if new_groups:
        #     instance.groups.clear()
        #     for group in new_groups:
        #         instance.groups.add(group)

        instance.save()
        return instance



class ConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailConfirmation
        fields = '__all__'

