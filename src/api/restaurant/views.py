from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

from restaurant.models import Restaurant, Review
from restaurant.serializers import (
    RestaurantSerializer, 
    ReviewSerializer, 
    RestaurantReviewSerializer
)


# Create your views here.
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = [IsAuthenticatedOrReadOnly, ]
        return super(ReviewViewSet, self).get_permissions()


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = RestaurantSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ['name']
    ordering_fields = ['score']

    @action(detail=True)
    def reviews(self, request, pk=None):
        instance = self.get_object()
        serializer = RestaurantReviewSerializer(instance.reviews.all(), many=True)
        return Response(serializer.data)
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'reviews']:
            self.permission_classes = [IsAuthenticatedOrReadOnly, ]
        return super(RestaurantViewSet, self).get_permissions()
    
    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(RestaurantViewSet, self).get_serializer(*args, **kwargs)
