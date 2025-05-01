# serializers.py
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'original_id', 'name', 'category', 'price', 
                 'description', 'image_url', 'brand', 'skin_type', 'concerns']
        extra_kwargs = {'description': {'source': 'concerns'}}