from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Place, Rent, RenterComment, PlaceImage
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from rest_framework.relations import HyperlinkedIdentityField

MAX_FILE_SIZE = 100


class GetCommentByLocatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RenterComment
        fields = ('facilities_score', 'cleanness_score', 'surroundings_score',
                  'price_achievement_score', 'locator_score', 'comment')


class RenterCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RenterComment
        fields = '__all__'
        read_only_fields = ('renter', 'place')

    def create(self, validated_data):
        validated_data["renter"] = self.context['request'].user
        place_id = self.context['view'].kwargs['parent_lookup_place']
        place = get_object_or_404(Place, id=place_id)
        validated_data["place"] = place
        rent = Rent.objects.filter(renter=validated_data['renter'], place=validated_data['place'], status='r')
        if not rent.exists():
            raise PermissionDenied

        renter_comment = RenterComment.objects.create(**validated_data)
        return renter_comment


class RentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = '__all__'
        read_only_fields = ('renter',)
        lookup_url_kwarg = "id"

    def create(self, validated_data):
        validated_data["renter"] = self.context['request'].user
        rent = Rent.objects.create(**validated_data)
        return rent


class UpdatePlaceByLocatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'
        read_only_fields = ('user', 'province', 'city', 'address', 'year_of_construction', 'place_type',
                            'home_document_file')


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        validated_data["user_id"] = self.context['request'].user.id
        place = Place.objects.create(**validated_data)
        return place


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
        read_only_fields = ('place',)
        lookup_url_kwarg = "id"

    def validate_image(self, file):
        if file.size > MAX_FILE_SIZE * 1024 * 1024:
            raise ValidationError("File too large ( > {0}Mb )".format(MAX_FILE_SIZE))
        return file
