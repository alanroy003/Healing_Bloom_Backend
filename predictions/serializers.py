# predictions/serializers.py
from rest_framework import serializers
from .models import PredictionHistory

class DiseaseDetailsSerializer(serializers.Serializer):
    symptoms = serializers.ListField(child=serializers.CharField())
    home_remedies = serializers.ListField(child=serializers.CharField())
    precautions = serializers.ListField(child=serializers.CharField())
    medicines = serializers.ListField(child=serializers.CharField())
    next_steps = serializers.ListField(child=serializers.CharField())

class PredictionHistorySerializer(serializers.ModelSerializer):
    disease_details = DiseaseDetailsSerializer(source='*')
    
    class Meta:
        model = PredictionHistory
        fields = [
            'id', 'image', 'predicted_class', 'disease_name', 
            'confidence', 'disease_details', 'created_at'
        ]
        read_only_fields = fields

class PredictionSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)