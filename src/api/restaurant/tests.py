from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from restaurant.models import Restaurant, Review

login = '/login/'

user1 = {
    'username': 'test1',
    'password': 'password123'
}
user2 = {
    'username': 'test2',
    'password': 'password321'
}

class RestaurantReviewTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.user1 = User.objects.create_user(**user1)
        cls.user2 = User.objects.create_user(**user2)
        cls.restaurant = Restaurant.objects.create(name='JE Kitchen')
        cls.review = Review.objects.create(
            title='JWP Kitchen',
            content='Delicious meal',
            score=5,
            user_id=cls.user1,
            restaurant_id=cls.restaurant
        )
        cls.client = APIClient()
        cls.token = cls.get_token()
        cls.restaurant_request_data = {
            'name': 'Kitchen island'
        }
        cls.review_request_data = {
            'title': 'I"d even seen....',
            'content': 'Worst service',
            'score': 1,
            'user_id': cls.user2.id,
            'restaurant_id': cls.restaurant.id
        }
    
    @classmethod
    def get_token(cls):
        response = cls.client.post(login, user1)
        return response.data['access']
    
    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    
    @classmethod
    def tearDownClass(cls):
        with transaction.atomic():
            User.objects.all().delete()
            Review.objects.all().delete()
            Restaurant.objects.all().delete()


class RestaurantTestCase(RestaurantReviewTestCase):
    url = '/restaurant/'
    restaurant_detail = '/restaurant/{}/'
    restaurant_search = '/restaurant/?search={}'
    restaurant_review_detail = '/restaurant/{}/reviews/'
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
    def test_restaurant_retrieve(self):
        restaurant = Restaurant.objects.get(pk=self.restaurant.id)
        response = self.client.get(self.restaurant_detail.format(self.restaurant.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name', None), restaurant.name)
        self.assertEqual(response.data.get('score', None), 5.0)
        self.assertEqual(response.data.get('review_count', None), 1)

    def test_restaurant_create(self):
        response = self.client.post(self.url, self.restaurant_request_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 2)
        self.assertEqual(response.data.get('name', None), self.restaurant_request_data['name'])

    def test_restaurant_update(self):
        test_data = {'name': 'JWP Kitchen'}
        response = self.client.put(self.restaurant_detail.format(self.restaurant.id), test_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name', None), test_data.get('name'))
    
    def test_restaurant_search(self):
        response = self.client.get(self.restaurant_search.format('Kitchen'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIsInstance(response.data['results'], list)
        self.assertTrue(len(response.data['results']) > 0)

        result = response.data['results'][0]
        self.assertIn('name', result)
        self.assertIn('review_count', result)
        self.assertIn('score', result)
        
    def test_restaurant_delete(self):
        response = self.client.delete(self.restaurant_detail.format(self.restaurant.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_restaurant_review_retrieve(self):
        response = self.client.get(self.restaurant_review_detail.format(self.restaurant.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertTrue(len(response.data) > 0)  


class ReviewTestCase(RestaurantReviewTestCase):
    url = '/review/'
    review_detail = '/review/{}/'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
    def test_review_retrieve(self):
        review = Review.objects.get(pk=self.review.id)
        response = self.client.get(self.review_detail.format(self.review.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title', None), review.title)
        self.assertEqual(response.data.get('content', None), review.content)
        self.assertEqual(response.data.get('score', None), review.score)

    def test_review_create(self):
        response = self.client.post(self.url, self.review_request_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)
        self.assertEqual(response.data.get('title', None), self.review_request_data['title'])
        self.assertEqual(response.data.get('content', None), self.review_request_data['content'])
        self.assertEqual(response.data.get('score', None), self.review_request_data['score'])

    def test_review_update(self):
        test_data = {
            'title': 'Delicious food',
            'content': 'Best service',
            'score':5,
            'user_id': self.user2.id,
            'restaurant_id': self.restaurant.id
        }
        response = self.client.put(self.review_detail.format(self.review.id), test_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title', None), test_data['title'])
        self.assertEqual(response.data.get('content', None), test_data['content'])
        self.assertEqual(response.data.get('score', None), test_data['score'])

    def test_review_delete(self):
        response = self.client.delete(self.review_detail.format(self.review.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
