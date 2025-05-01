# predictions/models.py
from django.db import models
from accounts.models import CustomUser

class PredictionHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='predictions')
    image = models.ImageField(upload_to='prediction_images/')
    predicted_class = models.CharField(max_length=10)  # Short code (e.g., AKIEC)
    disease_name = models.CharField(max_length=255)
    confidence = models.FloatField()
    symptoms = models.JSONField()
    home_remedies = models.JSONField()
    precautions = models.JSONField()
    medicines = models.JSONField()
    next_steps = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.disease_name} ({self.confidence:.2%})"