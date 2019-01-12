from django.db import models
from user_profile.models import DefaultUser


def upload_update_image(instance, filename):
    return "media/{user}/{filename}".format(user=instance.user, filename=filename)


class Post(models.Model):
    class Meta:
        verbose_name_plural = 'Posts'
        ordering = ('-updated',)

    user = models.ForeignKey(DefaultUser, related_name='User', on_delete=models.CASCADE,)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_update_image, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

