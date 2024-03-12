from django.db.models import Avg, Count
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from restaurant.models import Restaurant, Review
        

class ReviewSerializer(serializers.ModelSerializer):
    def validate_score(self, score):
        if score < 0 or score > 5:
            raise serializers.ValidationError("Score must between 1 and 5")
        return score
    
    class Meta:
        model = Review
        fields = ('id', 'title', 'content', 'score', 'restaurant_id', 'user_id')

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['user_id', 'restaurant_id']
            )
        ]


class RestaurantReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ['restaurant_id', 'created_time', 'updated_time'] 


class RestaurantListSerializer(serializers.ListSerializer):
    
    def create(self, validated_data):
        restaurants = [Restaurant(**item) for item in validated_data]
        return Restaurant.objects.bulk_create(restaurants)


class RestaurantSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators = [
            UniqueValidator(
                queryset=Restaurant.objects.all()
            )
        ]
    )
    
    def to_representation(self, value):
        data = super().to_representation(value)

        reviews = Restaurant.objects.annotate(
            count=Count('reviews'),
            score=Avg('reviews__score')
        ).get(pk=value.pk)
        
        data['review_count'] = reviews.count
        data['score'] = reviews.score if reviews.score else 0
        
        return data
    
    class Meta:
        model = Restaurant
        list_serializer_class = RestaurantListSerializer
        fields = ('id', 'name', )
        read_only_fields = ('id', 'created_time', 'updated_time', )
        depth = 1
