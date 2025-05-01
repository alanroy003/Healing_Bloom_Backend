# models.py
from django.db import models

class Product(models.Model):
    original_id = models.IntegerField()
    category = models.CharField(max_length=100)
    url = models.URLField()
    brand = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    skin_type = models.CharField(max_length=100)
    concerns = models.TextField()  # Will store comma-separated values
    image_url = models.URLField()

    def __str__(self):
        return self.name