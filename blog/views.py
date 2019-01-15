from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from blog.models import Post
from blog.permissions import IsPostOwner
from .serializers import PostSerializer


class PostAPIView(ModelViewSet):
    """
    list:
    Return a list of all posts

    create:
    Create a new post. Instanse - user

    retrieve (with post.id):
    Return the given post

    put (with post.id):
    Update or patch given post. Available for Post owner

    delete(with post.id):
    Delete post. Available for Post owner
    """
    permission_classes = (permissions.IsAuthenticated, IsPostOwner,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, *args, **kwargs):
        """
        post:
        Set like to Post from auth user
        """
        obj = self.get_object()
        obj.add_like(request.user)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['DELETE'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, *args, **kwargs):
        """
        delete:
        Delete like to Post from auth user
        """
        obj = self.get_object()
        obj.unlike(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
