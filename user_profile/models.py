from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class DefaultUserManager(BaseUserManager):

    def create_user(self, email, password):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class DefaultUser(AbstractBaseUser):

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    name = models.CharField(max_length=255, default='')

    is_admin = models.BooleanField(default=False)

    objects = DefaultUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin



