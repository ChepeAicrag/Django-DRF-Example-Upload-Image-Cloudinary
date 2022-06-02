from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


def upload_load(instance, filename):
    return f'photos_users/{instance.email}/{filename}'


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(
            email=self.normalize_email(email),
            name=extra_fields.get('name', None),
            phone=extra_fields.get('phone', None)
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.model(
            email=self.normalize_email(email),
            is_active=True,
            is_superuser=True,
            is_staff=True,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=150, null=False, verbose_name='name',)
    email = models.EmailField(
        unique=True, max_length=100, null=False, verbose_name='email',)
    phone = models.CharField(verbose_name='phone', max_length=10)
    image = models.ImageField(upload_to=upload_load, default='default.jpg',
                              max_length=255, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    status_delete = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'user'
        ordering = ('id',)

    def __str__(self):
        return f'{self.name} {self.email}'
