from django.contrib.auth.models import User

from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

from user.serializers import UserReviewSerializer
from user.serializers import UserSerializer, RegisterSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAdminUser, ]
        return super(UserViewSet, self).get_permissions()

    @action(detail=True)
    def reviews(self, request, pk=None):
        instance = self.get_object()
        serializer = UserReviewSerializer(instance.reviews.all(), many=True)
        return Response(serializer.data)
    

class RegisterViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
