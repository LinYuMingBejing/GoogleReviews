from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from restaurant.models import Restaurant, Review

# Create your tests here.
class UserTestCase(APITestCase):
    url = '/user/'
    login = '/login/'
    register = '/register/'
    test_data = {
        'username': 'test2',
        'password': 'password321',
        'password2': 'password321',
        'email': 'carrier2@gmail.com',
        'first_name': '',
        'last_name': ''
    }
    
    def setUp(self):
        self.client = APIClient()
        
    def test_user_register(self):
        response = self.client.post(self.register, self.test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('username', None), self.test_data.get('username'))
        self.assertEqual(response.data.get('email', None), self.test_data.get('email'))
        self.assertEqual(response.data.get('first_name', None), self.test_data.get('first_name'))
        self.assertEqual(response.data.get('last_name', None), self.test_data.get('last_name'))

    def test_user_login(self):
        register = self.client.post(self.register, self.test_data)
        response = self.client.post(self.login, self.test_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('refresh', None))
        self.assertIsNotNone(response.data.get('access', None))


class UserReviewTestCase(APITestCase):
    login = '/login/'
    user_detail = '/user/{}/'
    user_review_detail = '/user/{}/reviews/'
    test_data = {
        'username': 'test2',
        'password': 'password321'
    }

    def setUp(self):
        self.user1 = User.objects.create_user(**self.test_data)
        self.restaurant = Restaurant.objects.create(name='JE Kitchen')
        self.review = Review.objects.create(
            title='JWP Kitchen',
            content='Delicious meal',
            score=5,
            user_id=self.user1,
            restaurant_id=self.restaurant
        )
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_token()}')
    
    def get_token(self):
        response = self.client.post(self.login, self.test_data)
        return response.data['access']
            
    def test_user_retrive(self):
        response = self.client.get(self.user_detail.format(self.user1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('username', None), self.user1.username)
        self.assertEqual(response.data.get('email', None), self.user1.email)

    def test_user_review_retrieve(self):
        response = self.client.get(self.user_review_detail.format(self.user1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)       
        self.assertIsInstance(response.data, list)
        self.assertTrue(len(response.data) > 0)  