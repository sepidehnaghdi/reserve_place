from django.test import TestCase

from rest_framework.test import APITestCase
import json
from rest_framework.test import APIClient
from rest_framework import status
from .models import RenterProfile


class RenterProfileTestCase(APITestCase):
    fixtures = ['test_renter_app.json']
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

    def test_get_renter_profiles(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/renters"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_renter_profile_other_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/renters/3"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_renter_profile_user_himself(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/renters/2"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_renter_profile(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/renters/2"
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_renter_profile_other_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/renters/3"
        data = {
        }
        response = client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_renter_profile(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        locator_profile = RenterProfile.objects.get(user=2)
        self.assertEqual(locator_profile.birth_certificate_number, "11111")

        url = "/api/v1/renters/2"
        data = {
            "birth_certificate_number": "222222"
        }
        response = client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        locator_profile = RenterProfile.objects.get(user=2)
        self.assertEqual(locator_profile.birth_certificate_number, "222222")

    def test_put_renter_profile(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        locator_profile = RenterProfile.objects.get(user=2)
        self.assertEqual(locator_profile.birth_certificate_number, "11111")

        url = "/api/v1/renters/2"
        with open('/Users/sepidehnaghdi/Desktop/reserve_place/reserve_place/locator/tests.py') as fp, \
                open('/Users/sepidehnaghdi/Desktop/reserve_place/reserve_place/locator/tests.py') as fp1:
            data = {
                "contact_number": "333",
                "Second_contact_number": "3333",
                "relative_contact_number": "3333",

                "birth_certificate_number": "33333",
                "national_number": "3333",

                "image_of_birth_certificate": fp,
                "image_of_national_card": fp1
            }
            response = client.put(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            locator_profile = RenterProfile.objects.get(user=2)
            self.assertEqual(locator_profile.birth_certificate_number, "33333")


class RenterProfileBySuperUserTestCase(APITestCase):
    fixtures = ['test_renter_app.json']
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

    def test_get_renter_profiles(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/renters"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_renter_profile_other_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/renters/3"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_renter_profile(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/renters/2"
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_renter_profile_other_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        locator_profile = RenterProfile.objects.get(user=2)
        self.assertEqual(locator_profile.birth_certificate_number, "11111")

        url = "/api/v1/renters/2"
        data = {
            "birth_certificate_number": "222222"
        }
        response = client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        locator_profile = RenterProfile.objects.get(user=2)
        self.assertEqual(locator_profile.birth_certificate_number, "222222")

    def test_put_renter_profile(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        locator_profile = RenterProfile.objects.get(user=2)
        self.assertEqual(locator_profile.birth_certificate_number, "11111")

        url = "/api/v1/renters/2"
        with open('/Users/sepidehnaghdi/Desktop/reserve_place/reserve_place/locator/tests.py') as fp, \
                open('/Users/sepidehnaghdi/Desktop/reserve_place/reserve_place/locator/tests.py') as fp1:
            data = {
                "contact_number": "333",
                "Second_contact_number": "3333",
                "relative_contact_number": "3333",

                "birth_certificate_number": "33333",
                "national_number": "3333",

                "image_of_birth_certificate": fp,
                "image_of_national_card": fp1
            }
            response = client.put(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            locator_profile = RenterProfile.objects.get(user=2)
            self.assertEqual(locator_profile.birth_certificate_number, "33333")

