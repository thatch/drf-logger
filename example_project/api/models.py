from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('Given username must need.')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **ext_fields):
        ext_fields.setdefault('is_staff', False)
        ext_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **ext_fields)

    def create_superuser(self, username, email, password, **ext_fields):
        ext_fields.setdefault('is_staff', True)
        ext_fields.setdefault('is_superuser', True)

        if ext_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if ext_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **ext_fields)


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(_('username'), max_length=150, unique=True)

    email = models.EmailField(_('email'))
    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_active = models.BooleanField(_('active'), default=True)

    objects = UserManager()

    EMAIL_FILED = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)


class Person(models.Model):

    name = models.CharField(max_length=128)
    age = models.IntegerField()
