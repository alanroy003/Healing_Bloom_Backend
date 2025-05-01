# HealingBloom_Backend\user_profile\models.py
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts.models import CustomUser
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile',
        primary_key=True
    )
    code_number = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        help_text='Auto-generated unique user code'
    )
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        null=True,
        blank=True,
        help_text='User profile picture'
    )
    allergies = models.JSONField(
        default=list,
        help_text='List of allergies stored as JSON array'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f"Profile of {self.user.email}"

    def save(self, *args, **kwargs):
        if not self.code_number:
            self.code_number = self._generate_unique_code()
        super().save(*args, **kwargs)

    def _generate_unique_code(self):
        return f'USER-{uuid.uuid4().hex[:8].upper()}'

# Signal handlers
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()