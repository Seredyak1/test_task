from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics

from user_profile.permissions import IsOwner
from .serializers import RegistrationSerializer, UserSerializer


class RegistrationsAPIView(generics.ListCreateAPIView):
    """
    get:
    Return a list of all the existing users.

    post:
    Create a new user instance.
    """

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Return a user detail

    put:
    Update or patch info about user

    delete:
    Delete user instance.
    """
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    serializer_class = UserSerializer
    queryset = User.objects.all()
