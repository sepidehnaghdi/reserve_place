import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

from place_app.models import Place, Rent


class RentByRenterTestCase(APITestCase):
    fixtures = ['test_place_app.json']
    token = None

    def setUp(self):
        url = "/api/v1/login"
        data = {
            "username": "user2",
            "password": "123qweASD"
        }
        response = self.client.post(url, data, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.token = result['token']

    def test_rent_place_post(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        url = "/api/v1/rents"
        data = {
            'place': 1,
            'check_in_date': "2017-02-20",
            'check_out_date': "2017-02-25"

        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_rent_place_patch(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        rent = Rent.objects.create(
            renter_id=2,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25"
        )
        url = "/api/v1/rents"
        data = {
            'place': 1,
            'check_in_date': "2017-02-20",
            'check_out_date': "2017-02-25"

        }
        response = client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_rent_place_delete(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25"
        )
        url = "/api/v1/rents/1"

        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_rent_place_list(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25"
        )
        url = "/api/v1/rents"

        response = client.get(url, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(result), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rent_place_retrieve(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25"
        )
        url = "/api/v1/rents/1"

        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rent_place_list2(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        rent = Rent.objects.create(
            id=1,
            renter_id=2,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25"
        )
        url = "/api/v1/rents"

        response = client.get(url, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(result), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rent_place_retrieve2(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        rent = Rent.objects.create(
            id=1,
            renter_id=2,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25"
        )
        url = "/api/v1/rents/1"

        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RentByLocatorTestCase(APITestCase):
    fixtures = ['test_place_app.json']
    token = None

    def setUp(self):
        url = "/api/v1/login"
        data = {
            "username": "user1",
            "password": "123qweASD"
        }
        response = self.client.post(url, data, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.token = result['token']

    def test_rent_place_post(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        url = "/api/v1/rents"
        data = {
            'place': 1,
            'check_in_date': "2017-02-20",
            'check_out_date': "2017-02-25"

        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_rent_place_patch(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        rent = Rent.objects.create(
            renter_id=2,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25"
        )
        url = "/api/v1/rents"
        data = {
            'place': 1,
            'check_in_date': "2017-02-20",
            'check_out_date': "2017-02-25"

        }
        response = client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_rent_place_delete(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25"
        )
        url = "/api/v1/rents/1"

        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_rent_place_list(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25"
        )
        url = "/api/v1/rents"

        response = client.get(url, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(result), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rent_place_retrieve(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25"
        )
        url = "/api/v1/rents/1"

        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rent_place_list2(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        rent = Rent.objects.create(
            id=1,
            renter_id=2,
            place_id=2,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25"
        )
        url = "/api/v1/rents"

        response = client.get(url, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(result), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rent_place_retrieve2(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        rent = Rent.objects.create(
            id=1,
            renter_id=2,
            place_id=2,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25"
        )
        url = "/api/v1/rents/1"

        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



class RentBySuperUserTestCase(APITestCase):
    fixtures = ['test_place_app.json']
    token = None

    def setUp(self):
        url = "/api/v1/login"
        data = {
            "username": "super_user",
            "password": "123qweASD"
        }
        response = self.client.post(url, data, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.token = result['token']

    def test_rent_place_post(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        url = "/api/v1/rents"
        data = {
            'place': 1,
            'check_in_date': "2017-02-20",
            'check_out_date': "2017-02-25"

        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_rent_place_patch(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        rent = Rent.objects.create(
            renter_id=2,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25"
        )
        url = "/api/v1/rents"
        data = {
            'place': 1,
            'check_in_date': "2017-02-20",
            'check_out_date': "2017-02-25"

        }
        response = client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_rent_place_delete(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25"
        )
        url = "/api/v1/rents/1"

        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_rent_place_list(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25"
        )
        url = "/api/v1/rents"

        response = client.get(url, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(result), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rent_place_retrieve(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25"
        )
        url = "/api/v1/rents/1"

        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PlaceByLocatorTestCase(APITestCase):
    fixtures = ['test_place_app.json']
    token = None

    def setUp(self):
        url = "/api/v1/login"
        data = {
            "username": "user1",
            "password": "123qweASD"
        }
        response = self.client.post(url, data, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.token = result['token']

    def test_get_places(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_place(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places/1"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_place(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        data = {}
        url = "/api/v1/places"
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_place(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places/1"
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_patch_place_not_allowed(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        with open('/Users/sepidehnaghdi/Desktop/reserve_place/reserve_place/locator/tests.py') as fp:

            place = Place.objects.get(id=1)
            self.assertEqual(place.province, 'isf')
            self.assertEqual(place.max_num_of_people, 10)

            data = {
                "province": "teh",
                "max_num_of_people": 13

            }

            url = "/api/v1/places/1"
            response = client.patch(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

            place = Place.objects.get(id=1)
            self.assertEqual(place.max_num_of_people, 10)

    def test_patch_place(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        with open('/Users/sepidehnaghdi/Desktop/reserve_place/reserve_place/locator/tests.py') as fp:

            place = Place.objects.get(id=1)
            self.assertEqual(place.max_num_of_people, 10)

            data = {
                "max_num_of_people": 13

            }

            url = "/api/v1/places/1"
            response = client.patch(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            place = Place.objects.get(id=1)
            self.assertEqual(place.max_num_of_people, 13)


class PlaceByRenterTestCase(APITestCase):
    fixtures = ['test_place_app.json']
    token = None

    def setUp(self):
        url = "/api/v1/login"
        data = {
            "username": "user2",
            "password": "123qweASD"
        }
        response = self.client.post(url, data, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.token = result['token']

    def test_get_places(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_place(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places/1"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_place(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        data = {}
        url = "/api/v1/places"
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_place(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places/1"
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_place(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        with open('/Users/sepidehnaghdi/Desktop/reserve_place/reserve_place/locator/tests.py') as fp:

            place = Place.objects.get(id=1)
            self.assertEqual(place.province, 'isf')
            data = {
                "province": "teh",

            }

            url = "/api/v1/places/1"
            response = client.patch(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

            place = Place.objects.get(id=1)
            self.assertEqual(place.province, 'isf')


class PlaceBySuperUserTestCase(APITestCase):
    fixtures = ['test_place_app.json']
    token = None

    def setUp(self):
        url = "/api/v1/login"
        data = {
            "username": "super_user",
            "password": "123qweASD"
        }
        response = self.client.post(url, data, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.token = result['token']

    def test_get_places(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_place(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places/1"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_place(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        with open('/Users/sepidehnaghdi/Desktop/reserve_place/reserve_place/locator/tests.py') as fp:

            data = {
                "id": 2,
                "province": "isf",
                "city": "shahin shahr",
                "address": "third street, no 12",
                "year_of_construction": 1390,
                "total_area": 200,
                "construction_area": 150,
                "num_of_bed_rooms": 2,
                "place_type": "h",
                "max_num_of_people": 10,
                "allowed_more_people": False,
                "allowed_pet": False,
                "start_rental_period": "2017-02-20",
                "end_rental_period": "2017-02-25",
                "price_per_night": 2000000,
                "assignment_time": "14:00",
                "delivery_time": "17:00",
                "price_for_each_more_person": 300000,
                "rental_conditions": "conditions",
                "description": "desc",
                "surroundings": "surroundings",
                "distance_from_store": 3423,
                "distance_from_restaurant": 2343,
                "home_document_file": fp
            }

            url = "/api/v1/places"
            response = client.post(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            place = Place.objects.filter(id=2)
            self.assertEqual(place.count(), 1)

    def test_delete_place(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places/1"
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_patch_place(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        with open('/Users/sepidehnaghdi/Desktop/reserve_place/reserve_place/locator/tests.py') as fp:

            place = Place.objects.get(id=1)
            self.assertEqual(place.province, 'isf')
            data = {
                "province": "teh",

            }

            url = "/api/v1/places/1"
            response = client.patch(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            place = Place.objects.get(id=1)
            self.assertEqual(place.province, 'teh')
