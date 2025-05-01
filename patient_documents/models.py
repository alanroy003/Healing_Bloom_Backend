# HealingBloom_Backend\patient_documents\models.py
from django.db import models
from django.core.validators import FileExtensionValidator
from accounts.models import CustomUser
from django.utils import timezone
import os

def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/documents/<filename>
    return f'user_{instance.user.id}/documents/{filename}'

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('PR', 'Prescription'),
        ('RE', 'Report'),
        ('IM', 'Imaging'),
        ('IN', 'Insurance'),
        ('OT', 'Other'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=2, choices=DOCUMENT_TYPES, default='OT')
    file = models.FileField(
        upload_to=user_directory_path,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx']),
        # Add custom file size validator in serializers
    ]
    )
    notes = models.TextField(blank=True, null=True)
    upload_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.user.email}"

    def filename(self):
        return os.path.basename(self.file.name)

    class Meta:
        ordering = ['-upload_date']
        indexes = [
            models.Index(fields=['user', 'document_type']),
        ]