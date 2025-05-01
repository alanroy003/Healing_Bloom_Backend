# HealingBloom_Backend\HealingBloom_Backend\urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # API Endpoints
    path('api/accounts/', include('accounts.urls')),
    # path('api/diseases/', include('diseases.urls')),
    path('api/profile/', include('user_profile.urls')),
    # path('api/skin-disease/', include('skin_disease.urls')),
    path('api/skin/', include('predictions.urls')),
    path('api/patient/', include('patient_documents.urls')),
    path('api/shopping/', include('med_Shopping.urls')),



]
# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)