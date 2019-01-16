from rest_framework import serializers

from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post"""
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at', 'like_count']
