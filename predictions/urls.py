# predictions/urls.py
from django.urls import path
from .views import SkinDiseasePredictAPI, PredictionHistoryAPI

urlpatterns = [
    path('predict/', SkinDiseasePredictAPI.as_view(), name='predict'),
    path('history/', PredictionHistoryAPI.as_view(), name='prediction-history'),
]