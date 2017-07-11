import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from .models import LocatorProfile

class LocatorProfileTestCase(APITestCase):
    fixtures = ['test_locator_app.json']
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

    def test_get_locator_profiles(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/locators"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_locator_profile_other_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/locators/3"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_locator_profile_user_himself(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/locators/2"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_locator_profile(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/locators/2"
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_locator_profile_other_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/locators/3"
        data = {
        }
        response = client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_locator_profile(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        locator_profile = LocatorProfile.objects.get(user=2)
        self.assertEqual(locator_profile.birth_certificate_number, "11111")

        url = "/api/v1/locators/2"
        data = {
            "birth_certificate_number": "222222"
        }
        response = client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        locator_profile = LocatorProfile.objects.get(user=2)
        self.assertEqual(locator_profile.birth_certificate_number, "222222")

    def test_put_locator_profile(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        locator_profile = LocatorProfile.objects.get(user=2)
        self.assertEqual(locator_profile.birth_certificate_number, "11111")

        url = "/api/v1/locators/2"
        with open('/Users/sepidehnaghdi/Desktop/reserve_place/reserve_place/locator/tests.py') as fp, \
                open('/Users/sepidehnaghdi/Desktop/reserve_place/reserve_place/locator/tests.py') as fp1, \
                open('/Users/sepidehnaghdi/Desktop/reserve_place/reserve_place/locator/tests.py') as fp2:
            data = {
                "contact_number": "333",
                "Second_contact_number": "3333",
                "relative_contact_number": "3333",

                "birth_certificate_number": "33333",
                "national_number": "3333",

                "image_of_birth_certificate": fp,
                "image_of_clearance": fp1,
                "image_of_national_card": fp2
            }
            response = client.put(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            locator_profile = LocatorProfile.objects.get(user=2)
            self.assertEqual(locator_profile.birth_certificate_number, "33333")


class LocatorProfileBySuperUserTestCase(APITestCase):
    fixtures = ['test_locator_app.json']
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

    def test_get_locator_profiles(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/locators"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_locator_profile_other_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/locators/3"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_locator_profile_user_himself(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/locators/2"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_locator_profile(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/locators/2"
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_patch_locator_profile_other_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        locator_profile = LocatorProfile.objects.get(user=2)
        self.assertEqual(locator_profile.birth_certificate_number, "11111")

        url = "/api/v1/locators/2"
        data = {
            "birth_certificate_number": "222222"
        }
        response = client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        locator_profile = LocatorProfile.objects.get(user=2)
        self.assertEqual(locator_profile.birth_certificate_number, "222222")

    def test_put_locator_profile(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        locator_profile = LocatorProfile.objects.get(user=2)
        self.assertEqual(locator_profile.birth_certificate_number, "11111")

        url = "/api/v1/locators/2"
        with open('/Users/sepidehnaghdi/Desktop/reserve_place/reserve_place/locator/tests.py') as fp, \
                open('/Users/sepidehnaghdi/Desktop/reserve_place/reserve_place/locator/tests.py') as fp1, \
                open('/Users/sepidehnaghdi/Desktop/reserve_place/reserve_place/locator/tests.py') as fp2:
            data = {
                "contact_number": "333",
                "Second_contact_number": "3333",
                "relative_contact_number": "3333",

                "birth_certificate_number": "33333",
                "national_number": "3333",

                "image_of_birth_certificate": fp,
                "image_of_clearance": fp1,
                "image_of_national_card": fp2
            }
            response = client.put(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            locator_profile = LocatorProfile.objects.get(user=2)
            self.assertEqual(locator_profile.birth_certificate_number, "33333")

    def test_register_user_and_put_profile(self):
        url = "/api/v1/register"
        group = dict()
        group['name'] = 'locator'
        data = {
            'id': 5,
            'username': 'sepideh',
            'password': '123qweASD',
            'first_name': 'sepideh',
            'last_name': 'naghdi',
            'email': 'sepideh@gmail.com',
            'groups': group
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.filter(id=5)
        self.assertEqual(user.count(), 1)
        self.assertEqual(user[0].groups.values_list('name', flat=True)[0], "locator")

        # create profile during create user
        locator_profile = LocatorProfile.objects.filter(user=user)
        self.assertEqual(locator_profile[0].contact_number, None)
        self.assertEqual(locator_profile.count(), 1)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        url = "/api/v1/locators/5"
        with open('/Users/sepidehnaghdi/Desktop/reserve_place/reserve_place/locator/tests.py') as fp, \
                open('/Users/sepidehnaghdi/Desktop/reserve_place/reserve_place/locator/tests.py') as fp1, \
                open('/Users/sepidehnaghdi/Desktop/reserve_place/reserve_place/locator/tests.py') as fp2:
            data = {
                "contact_number": "333",
                "Second_contact_number": "3333",
                "relative_contact_number": "3333",

                "birth_certificate_number": "33333",
                "national_number": "3333",

                "image_of_birth_certificate": fp,
                "image_of_clearance": fp1,
                "image_of_national_card": fp2
            }
            response = client.put(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            locator_profile = LocatorProfile.objects.get(user=5)
            self.assertEqual(locator_profile.contact_number, "333")

            self.assertEqual(locator_profile.birth_certificate_number, "33333")

