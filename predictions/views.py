# predictions/views.py
import json
import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from tensorflow.keras.applications.inception_resnet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import PredictionHistory
from .serializers import PredictionSerializer, PredictionHistorySerializer
from io import BytesIO

# Load disease details once
with open(settings.BASE_DIR / 'predictions/ml_model/skin_diseases_details.json') as f:
    DISEASE_DETAILS = json.load(f)

# Validate disease details structure
REQUIRED_KEYS = {'symptoms', 'home_remedies', 'precautions', 'medicines', 'next_steps'}
for key, value in DISEASE_DETAILS.items():
    if not REQUIRED_KEYS.issubset(value.keys()):
        raise ValueError(f"Invalid disease details structure for {key}")

# Load model once at startup
try:
    MODEL = load_model(settings.BASE_DIR / 'predictions/ml_model/final_model.keras')
except Exception as e:
    raise RuntimeError(f"Error loading ML model: {str(e)}")

CLASS_NAMES = ['AKIEC', 'BCC', 'BKL', 'DF', 'MEL', 'NV', 'VASC']

class SkinDiseasePredictAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PredictionSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            img_file = request.FILES['image']
            
            # Handle both InMemoryUploadedFile and temporary files
            if isinstance(img_file, InMemoryUploadedFile):
                img_bytes = img_file.read()
                img = load_img(BytesIO(img_bytes), target_size=(224, 224))
            else:
                img = load_img(img_file.temporary_file_path(), target_size=(224, 224))

            # Preprocess image
            x = img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            # Make prediction
            preds = MODEL.predict(x)
            class_idx = np.argmax(preds[0])
            confidence = float(np.max(preds[0]))
            predicted_class = CLASS_NAMES[class_idx]
            
            # Get disease details
            details = DISEASE_DETAILS.get(predicted_class)
            if not details:
                return Response({'error': 'Disease details not found'}, 
                              status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Create history record
            history = PredictionHistory.objects.create(
                user=request.user,
                image=img_file,
                predicted_class=predicted_class,
                disease_name=details['disease_name'],
                confidence=confidence,
                symptoms=details['symptoms'],
                home_remedies=details['home_remedies'],
                precautions=details['precautions'],
                medicines=details['medicines'],
                next_steps=details['next_steps']
            )

            return Response({
                'prediction_id': history.id,
                'disease_name': details['disease_name'],
                'confidence': confidence,
                'details': details
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PredictionHistoryAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PredictionHistorySerializer

    def get(self, request):
        try:
            queryset = PredictionHistory.objects.filter(user=request.user)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)