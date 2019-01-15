from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics

from user_profile.permissions import IsOwner
from .serializers import RegistrationSerializer, UserSerializer


class RegistrationsAPIView(generics.ListCreateAPIView):
    """Get POST method to create user.
    Allow any user (authenticated or not) to hit this endpoint."""
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Show detail about user by his id.
    GET for all authenticated user, PUT and DELETE just for owner of account."""
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    serializer_class = UserSerializer
    queryset = User.objects.all()
