from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Place, Rent, RenterComment, PlaceImage
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from rest_framework.relations import HyperlinkedIdentityField

MAX_FILE_SIZE = 100


class RenterCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RenterComment
        fields = '__all__'
        read_only_fields = ('renter', )

    def create(self, validated_data):
        validated_data["renter"] = self.context['request'].user
        rent = Rent.objects.filter(renter=validated_data['renter'], place=validated_data['place'], status='r')
        if not rent.exists():
            raise PermissionDenied

        renter_comment = RenterComment.objects.create(**validated_data)
        return renter_comment


class RentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = '__all__'
        read_only_fields = ('renter', )
        lookup_url_kwarg = "id"

    def create(self, validated_data):
        validated_data["renter"] = self.context['request'].user
        rent = Rent.objects.create(**validated_data)
        return rent


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'
        read_only_fields = ('user', )

    def create(self, validated_data):
        validated_data["user_id"] = self.context['request'].user.id
        place = Place.objects.create(**validated_data)
        return place

    def update(self, instance, validated_data):
        locator_not_allowed_fields = ['user', 'province', 'city', 'address', 'year_of_construction', 'place_type', 'home_document_file']
        for field in locator_not_allowed_fields:
            if field in validated_data and instance.user.id == self.context['request'].user.id:
                raise PermissionDenied

        if instance.user.id != self.context['request'].user.id and not self.context['request'].user.is_superuser:
            raise PermissionDenied

        instance.province = validated_data.get('province', instance.province)
        instance.city = validated_data.get('city', instance.city)
        instance.address = validated_data.get('address', instance.address)
        instance.year_of_construction = validated_data.get('year_of_construction', instance.year_of_construction)
        instance.place_type = validated_data.get('place_type', instance.place_type)
        instance.home_document_file = validated_data.get('home_document_file', instance.home_document_file)
        instance.total_area = validated_data.get('total_area', instance.total_area)
        instance.construction_area = validated_data.get('construction_area', instance.construction_area)
        instance.num_of_bed_rooms = validated_data.get('num_of_bed_rooms', instance.num_of_bed_rooms)
        instance.max_num_of_people = validated_data.get('max_num_of_people', instance.max_num_of_people)
        instance.allowed_more_people = validated_data.get('allowed_more_people', instance.allowed_more_people)
        instance.allowed_pet = validated_data.get('allowed_pet', instance.allowed_pet)
        instance.start_rental_period = validated_data.get('start_rental_period', instance.start_rental_period)
        instance.end_rental_period = validated_data.get('end_rental_period', instance.end_rental_period)
        instance.price_per_night = validated_data.get('price_per_night', instance.price_per_night)
        instance.assignment_time = validated_data.get('assignment_time', instance.assignment_time)
        instance.delivery_time = validated_data.get('delivery_time', instance.delivery_time)
        instance.price_for_each_more_person = validated_data.get('price_for_each_more_person', instance.price_for_each_more_person)
        instance.rental_conditions = validated_data.get('rental_conditions', instance.rental_conditions)
        instance.description = validated_data.get('description', instance.description)
        instance.services = validated_data.get('services', instance.services)
        instance.surroundings = validated_data.get('surroundings', instance.surroundings)
        instance.distance_from_store = validated_data.get('distance_from_store', instance.distance_from_store)
        instance.distance_from_restaurant = validated_data.get('distance_from_restaurant', instance.distance_from_restaurant)

        instance.save()
        return instance


class MultiplePKsHyperlinkedIdentityField(HyperlinkedIdentityField):
    lookup_fields = ['pk']

    def __init__(self, view_name=None, **kwargs):
        self.lookup_fields = kwargs.pop('lookup_fields', self.lookup_fields)
        self.lookup_url_kwargs = kwargs.pop('lookup_url_kwargs', self.lookup_fields)

        assert len(self.lookup_fields) == len(self.lookup_url_kwargs)

        super(MultiplePKsHyperlinkedIdentityField, self).__init__(view_name, **kwargs)

    def get_object(self, view_name, view_args, view_kwargs):
        """
        Return the object corresponding to a matched URL.
        Takes the matched URL conf arguments, and should return an
        object instance, or raise an `ObjectDoesNotExist` exception.
        """
        lookup_kwargs = {
            key: view_kwargs[url_key]
            for key, url_key in zip(self.lookup_fields, self.lookup_url_kwargs)
        }
        return self.get_queryset().get(**lookup_kwargs)

    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the URL that hyperlinks to the object.
        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        # Unsaved objects will not yet have a valid URL.
        if hasattr(obj, 'pk') and obj.pk is None:
            return None

        kwargs = {
            url_key: getattr(obj, key)
            for key, url_key in zip(self.lookup_fields, self.lookup_url_kwargs)
        }
        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)


class PlaceImageSerializer(serializers.ModelSerializer):
    image = serializers.FileField(write_only=True)
    url = MultiplePKsHyperlinkedIdentityField(
        view_name='place-image-detail',
        lookup_fields=['place', 'pk'],
        lookup_url_kwargs=['parent_lookup_place', 'pk']
    )

    class Meta:
        model = PlaceImage
        fields = '__all__'
        read_only_fields = ('place', )
        lookup_url_kwarg = "id"

    def validate_image(self, file):
        if file.size > MAX_FILE_SIZE * 1024 * 1024:
            raise ValidationError("File too large ( > {0}Mb )".format(MAX_FILE_SIZE))
        return file




