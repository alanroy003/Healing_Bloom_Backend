# HealingBloom_Backend\patient_documents\serializers.py
from rest_framework import serializers
from .models import Document
from accounts.models import CustomUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class FileValidator:
    def __init__(self, max_size=5242880, allowed_types=None):  # 5MB default
        self.max_size = max_size
        self.allowed_types = allowed_types or ['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx']

    def __call__(self, value):
        if value.size > self.max_size:
            raise ValidationError(_(f'File size exceeds {self.max_size/1024/1024}MB'))
        ext = value.name.split('.')[-1].lower()
        if ext not in self.allowed_types:
            raise ValidationError(_(f'File type {ext} is not allowed'))


class EmptySerializer(serializers.Serializer):
    pass

class DocumentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(validators=[FileValidator()])
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Document
        fields = ['id', 'user', 'document_type', 'file', 'notes', 'upload_date', 'updated_at']
        read_only_fields = ['id', 'upload_date', 'updated_at', 'user']

    def validate(self, data):
        user = self.context['request'].user
        if data.get('user') != user:
            raise serializers.ValidationError("You can only create documents for yourself")
        return data

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except Exception as e:
            raise serializers.ValidationError(
                {'file': f'Error uploading document: {str(e)}'}
            )

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except Exception as e:
            raise serializers.ValidationError(
                {'error': f'Error updating document: {str(e)}'}
            )