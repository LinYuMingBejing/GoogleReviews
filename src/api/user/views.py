from django.contrib.auth.models import User

from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from user.serializers import UserReviewSerializer
from user.serializers import UserSerializer, RegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True)
    def reviews(self, request, pk=None):
        instance = self.get_object()
        serializer = UserReviewSerializer(instance.reviews.all(), many=True)
        return Response(serializer.data)
    

class RegisterViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
