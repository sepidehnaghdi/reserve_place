import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

from place_app.models import Place, Rent, RenterComment, PlaceImage


class RenterCommentByRenterTestCase(APITestCase):
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

    def test_renter_comment_post_not_rent_before(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        url = "/api/v1/places/1/comments"
        data = {
            'facilities_score': "3",
            'cleanness_score': "3",
            'surroundings_score': "3",
            'price_achievement_score': "3",
            'locator_score': "3",
            'comment': "this is a test comment"
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_renter_comment_post(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25",
            status='r'
        )

        url = "/api/v1/places/1/comments"
        data = {
            'facilities_score': 3,
            'cleanness_score': 3,
            'surroundings_score': 3,
            'price_achievement_score': 3,
            'locator_score': 3,
            'comment': "this is a test comment"
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_renter_comment_delete(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25",
            status='r'
        )

        RenterComment.objects.create(
            id=1,
            place_id=1,
            renter_id=3,
            facilities_score=3,
            cleanness_score=3,
            surroundings_score=3,
            price_achievement_score=3,
            locator_score=3,
            comment="this is a test comment"
        )

        url = "/api/v1/places/1/comments/1"

        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_renter_comment_patch(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25",
            status='r'
        )

        RenterComment.objects.create(
            id=1,
            place_id=1,
            renter_id=3,
            facilities_score=3,
            cleanness_score=3,
            surroundings_score=3,
            price_achievement_score=3,
            locator_score=3,
            comment="this is a test comment"
        )

        url = "/api/v1/places/1/comments/1"
        data = {
            'facilities_score': 4,
            'cleanness_score': 4,
        }

        response = client.patch(url, data, format='json')
        renter_comment = RenterComment.objects.get(id=1)
        self.assertEqual(renter_comment.facilities_score, 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_renter_comment_put(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25",
            status='r'
        )

        RenterComment.objects.create(
            id=1,
            place_id=1,
            renter_id=3,
            facilities_score=3,
            cleanness_score=3,
            surroundings_score=3,
            price_achievement_score=3,
            locator_score=3,
            comment="this is a test comment"
        )

        url = "/api/v1/places/1/comments/1"
        data = {
            'facilities_score': 4,
            'cleanness_score': 4,
            'surroundings_score': 4,
            'price_achievement_score': 4,
            'locator_score': 4,
            'comment': "this is a second test comment"
        }

        response = client.put(url, data, format='json')
        renter_comment = RenterComment.objects.get(id=1)
        self.assertEqual(renter_comment.facilities_score, 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_renter_comment_list(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25",
            status='r'
        )

        RenterComment.objects.create(
            id=1,
            place_id=1,
            renter_id=3,
            facilities_score=3,
            cleanness_score=3,
            surroundings_score=3,
            price_achievement_score=3,
            locator_score=3,
            comment="this is a test comment"
        )

        url = "/api/v1/places/1/comments"

        response = client.get(url, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(result), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_renter_comment_retrieve(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25",
            status='r'
        )

        RenterComment.objects.create(
            id=1,
            place_id=1,
            renter_id=3,
            facilities_score=3,
            cleanness_score=3,
            surroundings_score=3,
            price_achievement_score=3,
            locator_score=3,
            comment="this is a test comment"
        )

        url = "/api/v1/places/1/comments/1"

        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RenterCommentByLocatorTestCase(APITestCase):
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

    def test_renter_comment_post_not_rent_before(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        url = "/api/v1/places/1/comments"
        data = {
            'facilities_score': "3",
            'cleanness_score': "3",
            'surroundings_score': "3",
            'price_achievement_score': "3",
            'locator_score': "3",
            'comment': "this is a test comment"
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_renter_comment_post(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25",
            status='r'
        )

        url = "/api/v1/places/1/comments"
        data = {
            'facilities_score': 3,
            'cleanness_score': 3,
            'surroundings_score': 3,
            'price_achievement_score': 3,
            'locator_score': 3,
            'comment': "this is a test comment"
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_renter_comment_delete(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25",
            status='r'
        )

        RenterComment.objects.create(
            id=1,
            place_id=1,
            renter_id=3,
            facilities_score=3,
            cleanness_score=3,
            surroundings_score=3,
            price_achievement_score=3,
            locator_score=3,
            comment="this is a test comment"
        )

        url = "/api/v1/places/1/comments/1"

        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_renter_comment_patch(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25",
            status='r'
        )

        RenterComment.objects.create(
            id=1,
            place_id=1,
            renter_id=3,
            facilities_score=3,
            cleanness_score=3,
            surroundings_score=3,
            price_achievement_score=3,
            locator_score=3,
            comment="this is a test comment"
        )

        url = "/api/v1/places/1/comments/1"
        data = {
            'facilities_score': 4,
            'cleanness_score': 4,
        }

        response = client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_renter_comment_put(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25",
            status='r'
        )

        RenterComment.objects.create(
            id=1,
            place_id=1,
            renter_id=3,
            facilities_score=3,
            cleanness_score=3,
            surroundings_score=3,
            price_achievement_score=3,
            locator_score=3,
            comment="this is a test comment"
        )

        url = "/api/v1/places/1/comments/1"
        data = {
            'facilities_score': 4,
            'cleanness_score': 4,
            'surroundings_score': 4,
            'price_achievement_score': 4,
            'locator_score': 4,
            'comment': "this is a second test comment"
        }

        response = client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_renter_comment_list(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25",
            status='r'
        )

        RenterComment.objects.create(
            id=1,
            place_id=1,
            renter_id=3,
            facilities_score=3,
            cleanness_score=3,
            surroundings_score=3,
            price_achievement_score=3,
            locator_score=3,
            comment="this is a test comment"
        )

        url = "/api/v1/places/1/comments"

        response = client.get(url, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(result), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_renter_comment_retrieve(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25",
            status='r'
        )

        RenterComment.objects.create(
            id=1,
            place_id=1,
            renter_id=3,
            facilities_score=3,
            cleanness_score=3,
            surroundings_score=3,
            price_achievement_score=3,
            locator_score=3,
            comment="this is a test comment"
        )

        url = "/api/v1/places/1/comments/1"

        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RenterCommentBySuperUserTestCase(APITestCase):
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

    def test_renter_comment_post_not_rent_before(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        url = "/api/v1/places/1/comments"
        data = {
            'facilities_score': "3",
            'cleanness_score': "3",
            'surroundings_score': "3",
            'price_achievement_score': "3",
            'locator_score': "3",
            'comment': "this is a test comment"
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_renter_comment_post(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25",
            status='r'
        )

        url = "/api/v1/places/1/comments"
        data = {
            'facilities_score': 3,
            'cleanness_score': 3,
            'surroundings_score': 3,
            'price_achievement_score': 3,
            'locator_score': 3,
            'comment': "this is a test comment"
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_renter_comment_delete(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25",
            status='r'
        )

        RenterComment.objects.create(
            id=1,
            place_id=1,
            renter_id=3,
            facilities_score=3,
            cleanness_score=3,
            surroundings_score=3,
            price_achievement_score=3,
            locator_score=3,
            comment="this is a test comment"
        )

        url = "/api/v1/places/1/comments/1"

        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_renter_comment_patch(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25",
            status='r'
        )

        RenterComment.objects.create(
            id=1,
            place_id=1,
            renter_id=3,
            facilities_score=3,
            cleanness_score=3,
            surroundings_score=3,
            price_achievement_score=3,
            locator_score=3,
            comment="this is a test comment"
        )

        url = "/api/v1/places/1/comments/1"
        data = {
            'facilities_score': 4,
            'cleanness_score': 4,
        }

        response = client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_renter_comment_put(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25",
            status='r'
        )

        RenterComment.objects.create(
            id=1,
            place_id=1,
            renter_id=3,
            facilities_score=3,
            cleanness_score=3,
            surroundings_score=3,
            price_achievement_score=3,
            locator_score=3,
            comment="this is a test comment"
        )

        url = "/api/v1/places/1/comments/1"
        data = {
            'place': 1,
            'facilities_score': 4,
            'cleanness_score': 4,
            'surroundings_score': 4,
            'price_achievement_score': 4,
            'locator_score': 4,
            'comment': "this is a second test comment"
        }

        response = client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_renter_comment_list(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25",
            status='r'
        )

        RenterComment.objects.create(
            id=1,
            place_id=1,
            renter_id=3,
            facilities_score=3,
            cleanness_score=3,
            surroundings_score=3,
            price_achievement_score=3,
            locator_score=3,
            comment="this is a test comment"
        )

        url = "/api/v1/places/1/comments"

        response = client.get(url, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(result), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_renter_comment_retrieve(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25",
            status='r'
        )

        RenterComment.objects.create(
            id=1,
            place_id=1,
            renter_id=3,
            facilities_score=3,
            cleanness_score=3,
            surroundings_score=3,
            price_achievement_score=3,
            locator_score=3,
            comment="this is a test comment"
        )

        url = "/api/v1/places/1/comments/1"

        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


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

    def test_rent_place_post_out_of_range(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        url = "/api/v1/rents"
        data = {
            'place': 1,
            'check_in_date': "2017-02-15",
            'check_out_date': "2017-02-25"

        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rent_place_post_rent_before(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25",
            status='r'
        )

        url = "/api/v1/rents"
        data = {
            'place': 1,
            'check_in_date': "2017-02-20",
            'check_out_date': "2017-02-25"

        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

    def test_rent_place_delete_error(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25",
            status='r'
        )
        url = "/api/v1/rents/1"

        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

    def test_rent_place_list_by_place_not_rent(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25"
        )
        url = "/api/v1/rents?place=2"

        response = client.get(url, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(result), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rent_place_list_by_place(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25"
        )
        url = "/api/v1/rents?place=1"

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

    def test_rent_place_list_by_place_id(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25"
        )
        url = "/api/v1/rents?place=1"

        response = client.get(url, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(result), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rent_place_list_by_place_id2(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        rent = Rent.objects.create(
            id=1,
            renter_id=3,
            place_id=1,
            check_in_date="2017-02-20",
            check_out_date="2017-02-25"
        )
        url = "/api/v1/rents?place=3"

        response = client.get(url, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(result), 0)
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
            check_in_date="2017-02-16",
            check_out_date="2017-02-20"
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
            check_in_date="2017-02-16",
            check_out_date="2017-02-19"
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

    def test_get_places_by_province(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places?province=teh"
        response = client.get(url, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(result), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_places_by_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places?user__first_name=user3&user__last_name=userian3"
        response = client.get(url, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(result), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_places_by_address(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places?address__contains=no"
        response = client.get(url, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(result), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_places_by_start_rental_period(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places?start_rental_period__gte=2017-02-20"
        response = client.get(url, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(result), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_places_by_period1(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places?start_rental_period__gte=2017-02-20&end_rental_period__lte=2017-02-26"
        response = client.get(url, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(result), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_places_by_period2(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places?start_rental_period__gte=2017-02-15&end_rental_period__lte=2017-02-26"
        response = client.get(url, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(result), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_places_by_period3(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places?start_rental_period__gte=2017-02-20&end_rental_period__lte=2017-02-30"
        response = client.get(url, format='json')
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(result), 0)
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
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            place = Place.objects.get(id=1)
            self.assertEqual(place.max_num_of_people, 13)
            self.assertEqual(place.province, 'isf')


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


class PlaceImageByLocatorTestCase(APITestCase):
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

    def test_post_place_image(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        data = {}
        url = "/api/v1/places/1/images"
        with open('/Users/sepidehnaghdi/Desktop/reserve_place/reserve_place/locator/tests.py') as fp:
            data={
                'image': fp
            }

            response = client.post(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_place_image_for_place_of_other_locator(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        data = {}
        url = "/api/v1/places/2/images"
        with open('/Users/sepidehnaghdi/Desktop/reserve_place/reserve_place/locator/tests.py') as fp:
            data={
                'image': fp
            }

            response = client.post(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_image_places(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places/1/images"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_image_places(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places/1/images/2"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_place(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places/1/images/2"
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_patch_place_not_allowed(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        data = {}
        url = "/api/v1/places/1/images/2"
        response = client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_put_place_not_allowed(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        data = {}
        url = "/api/v1/places/1/images/2"
        response = client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class PlaceImageByRenterTestCase(APITestCase):
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

    def test_post_place(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        data = {}
        url = "/api/v1/places/1/images"
        with open('/Users/sepidehnaghdi/Desktop/reserve_place/reserve_place/locator/tests.py') as fp:
            data={
                'image': fp
            }

            response = client.post(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_image_places(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places/1/images"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_image_places(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places/1/images/2"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_place(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places/1/images/2"
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_place_not_allowed(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        data = {}
        url = "/api/v1/places/1/images/2"
        response = client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_put_place_not_allowed(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        data = {}
        url = "/api/v1/places/1/images/2"
        response = client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class PlaceImageBySuperUserTestCase(APITestCase):
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

    def test_post_place(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        data = {}
        url = "/api/v1/places/1/images"
        with open('/Users/sepidehnaghdi/Desktop/reserve_place/reserve_place/locator/tests.py') as fp:
            data={
                'image': fp
            }

            response = client.post(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_image_places(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places/1/images"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_image_places(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places/1/images/2"
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_place(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        url = "/api/v1/places/1/images/2"
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_patch_place_not_allowed(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        data = {}
        url = "/api/v1/places/1/images/2"
        response = client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_put_place_not_allowed(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        data = {}
        url = "/api/v1/places/1/images/2"
        response = client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
