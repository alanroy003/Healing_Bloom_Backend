from rest_framework import serializers
from .models import UserProfile
from accounts.models import CustomUser

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    allergies = serializers.ListField(
        child=serializers.CharField(max_length=255),
        allow_empty=True,
        required=False
    )

    class Meta:
        model = UserProfile
        fields = [
            'email',
            'username',
            'code_number',
            'profile_photo',
            'allergies',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['code_number', 'created_at', 'updated_at']

    def validate_allergies(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Allergies must be a list of strings")
        if any(not isinstance(item, str) or not item.strip() for item in value):
            raise serializers.ValidationError(
                "Allergies must contain non-empty strings"
            )
        return list(set(value))  # Remove duplicates

    def update(self, instance, validated_data):
        # Handle profile photo update
        if 'profile_photo' in validated_data:
            if instance.profile_photo:
                instance.profile_photo.delete(save=False)
            instance.profile_photo = validated_data.pop('profile_photo')
        
        # Handle allergies update
        if 'allergies' in validated_data:
            current_allergies = set(instance.allergies)
            new_allergies = set(validated_data.pop('allergies'))
            instance.allergies = list(current_allergies.union(new_allergies))

        return super().update(instance, validated_data)