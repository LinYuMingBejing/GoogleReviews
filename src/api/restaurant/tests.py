from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from restaurant.models import Restaurant, Review


class RestaurantReviewTestCase(APITestCase):
    login = '/login/'
    admin_account = {
        'username': 'root',
        'password': 'password123'
    }
    user1_account = {
        'username': 'test1',
        'password': 'password321'
    }
    user2_account = {
        'username': 'test2',
        'password': 'password321'
    }

    @classmethod
    def setUpClass(cls):
        cls.user1 = User.objects.create_user(**cls.user1_account)
        cls.user2 = User.objects.create_user(**cls.user2_account)
        cls.admin = User.objects.create_superuser(**cls.admin_account)
        cls.restaurant = Restaurant.objects.create(name='JE Kitchen')
        cls.review = Review.objects.create(
            title='JWP Kitchen',
            content='Delicious meal',
            score=5,
            user=cls.user1,
            restaurant=cls.restaurant
        )
        cls.client = APIClient()
        cls.user1_token = cls.get_token(cls.user1_account)
        cls.user2_token = cls.get_token(cls.user2_account)
        cls.admin_token = cls.get_token(cls.admin_account)
        
    @classmethod
    def get_token(cls, user):
        response = cls.client.post(cls.login, user)
        return response.data['access']
    
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

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
    def test_restaurant_retrieve(self):
        restaurant = Restaurant.objects.get(pk=self.restaurant.id)
        response = self.client.get(self.restaurant_detail.format(self.restaurant.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name', None), restaurant.name)
        self.assertEqual(response.data.get('score', None), 5.0)
        self.assertEqual(response.data.get('review_count', None), 1)

    def test_restaurant_create(self):
        test_data = {
            'name': 'Kitchen island'
        }
        response = self.client.post(self.url, test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 2)
        self.assertEqual(response.data.get('name', None), test_data['name'])

    def test_restaurant_create_with_bad_request(self):
        test_data = {
            'name': 'Kitchen island'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user1_token}')
        response = self.client.post(self.url, test_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_restaurant_update(self):
        test_data = {
            'name': 'JWP Kitchen'
        }
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

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user1_token}')
        
    def test_review_retrieve(self):
        review = Review.objects.get(pk=self.review.id)
        response = self.client.get(self.review_detail.format(self.review.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title', None), review.title)
        self.assertEqual(response.data.get('content', None), review.content)
        self.assertEqual(response.data.get('score', None), review.score)

    def test_review_create_with_duplicate_user_id(self):
        test_data = {
            'title': 'I"d even seen....',
            'content': 'Worst service',
            'score': 1,
            'user': self.user1.id,
            'restaurant': self.restaurant.id
        }
        response = self.client.post(self.url, test_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_with_bad_request(self):
        test_data = {
            'title': 'I"d even seen....',
            'content': 'Worst service',
            'score': 1,
            'user': self.user2.id,
            'restaurant': self.restaurant.id
        }
        response = self.client.post(self.url, test_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create(self):
        test_data = {
            'title': 'I"d even seen....',
            'content': 'Worst service',
            'score': 1,
            'user': self.user2.id,
            'restaurant': self.restaurant.id
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user2_token}')
        response = self.client.post(self.url, test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)
        self.assertEqual(response.data.get('title', None), test_data['title'])
        self.assertEqual(response.data.get('content', None), test_data['content'])
        self.assertEqual(response.data.get('score', None), test_data['score'])

    def test_review_update_with_bad_request(self):
        test_data = {
            'title': 'Delicious food',
            'content': 'Best service',
            'score': 5,
            'user': self.user2.id,
            'restaurant': self.restaurant.id
        }
        response = self.client.put(self.review_detail.format(self.review.id), test_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_update(self):
        test_data = {
            'title': 'Delicious food',
            'content': 'Best service',
            'score': 5,
            'user': self.user1.id,
            'restaurant': self.restaurant.id
        }
        response = self.client.put(self.review_detail.format(self.review.id), test_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title', None), test_data['title'])
        self.assertEqual(response.data.get('content', None), test_data['content'])
        self.assertEqual(response.data.get('score', None), test_data['score'])

    def test_review_delete(self):
        response = self.client.delete(self.review_detail.format(self.review.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
