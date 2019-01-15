from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from blog.models import Post
from blog.permissions import IsPostOwner
from .serializers import PostSerializer


class PostAPIView(ModelViewSet):
    """Main view. Show API for Post, Post Detail (by post.id), set like and unlike for post.
    Method POST and GET (post detail by id and list of posts) for all authenticated users,
    PUT and DELETE -> just for owners if Posts"""
    permission_classes = (permissions.IsAuthenticated, IsPostOwner,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, *args, **kwargs):
        """url: '/posts/post_id/like; set like for post"""
        obj = self.get_object()
        obj.add_like(request.user)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['DELETE'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, *args, **kwargs):
        """url: '/posts/post_id/unlike; delete like for post"""
        obj = self.get_object()
        obj.unlike(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
