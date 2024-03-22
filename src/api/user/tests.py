from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from restaurant.models import Restaurant, Review


# Create your tests here.
class UserTestCase(APITestCase):
    url = '/user/'
    login = '/login/'
    register = '/register/'

    user_account = {
        'username': 'test1',
        'password': 'password321A'
    }

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(**cls.user_account)
    
    def setUp(self):
        self.client = APIClient()
        
    def test_user_register_with_wrong_password(self):
        test_data = {
            'username': 'test2',
            'password': 'password321',
            'password2': 'password321',
            'email': 'cycarrier@gmail.com'
        }
        response = self.client.post(self.register, test_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        test_data['password'] = 'password321'
        test_data['password2'] = 'password3210'
        response = self.client.post(self.register, test_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_register(self):
        test_data = {
            'username': 'test2',
            'password': 'password321A',
            'password2': 'password321A',
            'email': 'cycarrier@gmail.com',
            'first_name': '',
            'last_name': ''
        }
        response = self.client.post(self.register, test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('username', None), test_data.get('username'))
        self.assertEqual(response.data.get('email', None), test_data.get('email'))
        self.assertEqual(response.data.get('first_name', None), test_data.get('first_name'))
        self.assertEqual(response.data.get('last_name', None), test_data.get('last_name'))

    def test_user_login(self):
        response = self.client.post(self.login, self.user_account)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('refresh', None))
        self.assertIsNotNone(response.data.get('access', None))
    
    @classmethod
    def tearDownClass(cls):
        with transaction.atomic():
            User.objects.all().delete()


class UserReviewTestCase(APITestCase):
    login = '/login/'
    user_detail = '/user/{}/'
    user_review_detail = '/user/{}/reviews/'
    user_account = {
        'username': 'test2',
        'password': 'password321A'
    }
    admin_account = {
        'username': 'root',
        'password': 'password123'
    }

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(**cls.user_account)
        cls.admin = User.objects.create_superuser(**cls.admin_account)
        cls.restaurant = Restaurant.objects.create(name='JE Kitchen')
        cls.review = Review.objects.create(
            title='JWP Kitchen',
            content='Delicious meal',
            score=5,
            user=cls.user,
            restaurant=cls.restaurant
        )
        cls.client = APIClient()
        cls.user_token = cls.get_token(cls.user_account)
        cls.admin_token = cls.get_token(cls.admin_account)
        
    @classmethod
    def get_token(cls, user):
        response = cls.client.post(cls.login, user)
        return response.data['access']
    
    def test_user_retrive(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(self.user_detail.format(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('username', None), self.user.username)
        self.assertEqual(response.data.get('email', None), self.user.email)
    
    def test_user_retrive_with_no_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        response = self.client.get(self.user_detail.format(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_review_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        response = self.client.get(self.user_review_detail.format(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIsInstance(response.data['results'], list)
        self.assertTrue(len(response.data['results']) > 0)
    
    @classmethod
    def tearDownClass(cls):
        with transaction.atomic():
            User.objects.all().delete()
            Review.objects.all().delete()
            Restaurant.objects.all().delete()