from django.contrib.auth.models import User

from rest_framework import generics, viewsets, status
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
        try:
            instance = User.objects.prefetch_related('reviews').get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        reviews = self.paginate_queryset(instance.reviews.all())
        serializer = UserReviewSerializer(reviews, many=True)
        return self.get_paginated_response(serializer.data)
    

class RegisterViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
