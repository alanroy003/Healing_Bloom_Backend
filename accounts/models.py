# HealingBloom_Backend\accounts\models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class CustomUser(AbstractUser):
    class UserType(models.IntegerChoices):
        ADMIN = 1, _('Admin')
        REGULAR_USER = 2, _('Regular User')

    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _('A user with that email already exists.'),
        }
    )
    user_type = models.PositiveSmallIntegerField(
        choices=UserType.choices,
        default=UserType.REGULAR_USER
    )
    is_verified = models.BooleanField(_('verified'), default=False)
    created_at = models.DateTimeField(
        _('Creation Date'),
        default=timezone.now,
        editable=False,
        help_text='Timestamp of creation'
    )
    updated_at = models.DateTimeField(
        _('Last Updated'),
        auto_now=True,
        help_text='Timestamp of last update'
    )

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        get_latest_by = 'created_at'
        ordering = ['-created_at']


    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.email = self.__class__.objects.normalize_email(self.email)
        super().save(*args, **kwargs)