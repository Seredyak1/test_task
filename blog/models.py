from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    """Main model of app. Related with user, and user is required parameter"""
    class Meta:
        verbose_name_plural = 'Posts'
        ordering = ('-updated',)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def like_count(self):
        """Get number of likes for Post"""
        return self.like_set.count()

    def add_like(self, user):
        """Add like to this Post"""
        Like.objects.get_or_create(user=user, post=self)

    def unlike(self, user):
        """Delete like to this Post"""
        Like.objects.filter(user=user, post=self).delete()


class Like(models.Model):
    """Related with user and Post"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
