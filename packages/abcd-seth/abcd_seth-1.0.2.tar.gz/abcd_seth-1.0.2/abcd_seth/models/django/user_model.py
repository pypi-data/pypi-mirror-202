from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

import abcd_seth.abcd.models.domain as domain_models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email=email,
            password=password,
            name=name,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = 'auth_user'

    def update_from_domain(self, user_domain: domain_models.User) -> None:
        try:
            user = User.objects.get(email=user_domain.email)
        except User.DoesNotExist:
            user = User()
        user.name = user_domain.name
        user.email = user_domain.email
        user.password = user_domain.password
        user.save()

    def to_domain(self) -> domain_models.User:
        return domain_models.User(
            name=self.name,
            email=self.email,
            password=self.password,
            created_at=self.created_at,
        )
