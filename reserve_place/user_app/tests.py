import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from locator.models import LocatorProfile

class RegisterTestCase(APITestCase):
    fixtures = ['test_user_app.json']

    def test_register_user_with_default_group(self):
        url = "/api/v1/register"
        data = {
            'id': 3,
            'username': 'sepideh',
            'password': '123qweASD',
            'first_name': 'sepideh',
            'last_name': 'naghdi',
            'email': 'sepideh@gmail.com'

        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(id=3)
        self.assertEqual(user.count(), 0)



    def test_register_user_with_invalid_group(self):
        url = "/api/v1/register"
        group = dict()
        group['name'] = 'locatorr'
        data = {
            'id': 3,
            'username': 'sepideh',
            'password': '123qweASD',
            'first_name': 'sepideh',
            'last_name': 'naghdi',
            'email': 'sepideh@gmail.com',
            'groups': group
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(id=3)
        self.assertEqual(user.count(), 0)

    def test_register_user_with_valid_group(self):
        url = "/api/v1/register"
        group = dict()
        group['name'] = 'locator'
        data = {
            'id': 3,
            'username': 'sepideh',
            'password': '123qweASD',
            'first_name': 'sepideh',
            'last_name': 'naghdi',
            'email': 'sepideh@gmail.com',
            'groups': group
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.filter(id=3)
        self.assertEqual(user.count(), 1)
        self.assertEqual(user[0].groups.values_list('name', flat=True)[0], "locator")

        # create profile during create user
        locator_profile = LocatorProfile.objects.filter(user=user)
        self.assertEqual(locator_profile.count(),1)


    def test_get_register_view(self):
        url = "/api/v1/register"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class UserNotAuthTestCase(APITestCase):
    fixtures = ['test_user_app.json']

    def test_get_users_without_auth(self):
        url = "/api/v1/users"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserBySuperUserTestCase(APITestCase):
    fixtures = ['test_user_app.json']
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

    def test_get_users(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/users"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/users/2"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        user = User.objects.filter(id=2)
        self.assertEqual(user.count(), 1)

        locator_profile = LocatorProfile.objects.filter(user__id=2)
        self.assertEqual(locator_profile.count(), 1)

        url = "/api/v1/users/2"
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        user = User.objects.filter(id=2)
        self.assertEqual(user.count(), 1)

        locator_profile = LocatorProfile.objects.filter(user__id=2)
        self.assertEqual(locator_profile.count(), 1)

    def test_update_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        data = {
            'first_name': 'sepideh',
            'last_name': 'naghdi',
        }
        url = "/api/v1/users/2"
        response = client.patch(url, data, format='json')

        user = User.objects.get(id=2)
        self.assertEqual(user.first_name, "sepideh")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        data = {
            'first_name': 'sepideh',
            'last_name': 'naghdi',
            'email': 'test@test.com',
            'password': '123qwe!'
        }
        url = "/api/v1/users/2"
        response = client.put(url, data, format='json')

        user = User.objects.get(id=2)
        self.assertEqual(user.first_name, "sepideh")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update_user_username(self):
        # cannot update username
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        data = {
            'username': 'sepideh',
        }
        url = "/api/v1/users/2"
        response = client.patch(url, data, format='json')
        user = User.objects.get(id=2)
        self.assertEqual(user.username, "user1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_password(self):
        url = "/api/v1/login"
        data = {
            "username": "user1",
            "password": "123qweASD"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        data = {
            'password': '123qwe!',
        }
        url = "/api/v1/users/2"
        response = client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = "/api/v1/login"
        data = {
            "username": "user1",
            "password": "123qweASD"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        url = "/api/v1/login"
        data = {
            "username": "user1",
            "password": "123qwe!"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/users"
        data = {}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserByNotSuperUserTestCase(APITestCase):
    fixtures = ['test_user_app.json']
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

    def test_get_users(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/users"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        url = "/api/v1/users/2"
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/users/2"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_other_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/users/1"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        data = {
            'first_name': 'sepideh',
            'last_name': 'naghdi',
        }
        url = "/api/v1/users/2"
        response = client.patch(url, data, format='json')

        user = User.objects.get(id=2)
        self.assertEqual(user.first_name, "sepideh")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_group(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        data = {
            'groups': [2],
        }
        url = "/api/v1/users/2"
        response = client.patch(url, data, format='json')
        user = User.objects.get(id=2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.groups.values_list('name', flat=True)[0], "locator")

    def test_update_other_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        data = {
            'first_name': 'sepideh',
            'last_name': 'naghdi',
        }
        url = "/api/v1/users/1"
        response = client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_username(self):
        # cannot update username
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        data = {
            'username': 'sepideh',
        }
        url = "/api/v1/users/2"
        response = client.patch(url, data, format='json')
        user = User.objects.get(id=2)
        self.assertEqual(user.username, "user1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_password(self):
        url = "/api/v1/login"
        data = {
            "username": "user1",
            "password": "123qweASD"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        data = {
            'password': '123qwe!',
        }
        url = "/api/v1/users/2"
        response = client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = "/api/v1/login"
        data = {
            "username": "user1",
            "password": "123qweASD"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        url = "/api/v1/login"
        data = {
            "username": "user1",
            "password": "123qwe!"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/users"
        data = {}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GroupSuperUserTestCase(APITestCase):
    fixtures = ['test_user_app.json']
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

    def test_get_groups(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/groups"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_group(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/groups/1"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_exist_group(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/groups"
        data = {
            'name': 'renter'
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_group(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/groups"
        data = {
            'name': 'others'
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_group(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        group = Group.objects.get(id=1)
        self.assertEqual(group.name, 'locator')
        url = "/api/v1/groups/1"
        data = {
            'name': 'others'
        }
        response = client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        group = Group.objects.get(id=1)
        self.assertEqual(group.name, 'others')

    def test_patch_group(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        group = Group.objects.get(id=1)
        self.assertEqual(group.name, 'locator')
        url = "/api/v1/groups/1"
        data = {
            'name': 'others'
        }
        response = client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        group = Group.objects.get(id=1)
        self.assertEqual(group.name, 'others')

    def test_delete_group(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        group = Group.objects.get(id=1)
        self.assertEqual(group.name, 'locator')
        url = "/api/v1/groups/1"

        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        group = Group.objects.filter(id=1)
        self.assertEqual(group.count(), 0)


class LoginTestCase(APITestCase):
    fixtures = ['test_user_app.json']

    def test_login(self):
        url = "/api/v1/login"
        data = {
            "username": "super_user",
            "password": "123qweASD"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_error(self):
        url = "/api/v1/login"
        data = {
            "username": "super_use",
            "password": "123qweASD"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_error2(self):
        url = "/api/v1/login"
        data = {
            "username": "super_use",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_method_for_login_url(self):
        url = "/api/v1/login"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
