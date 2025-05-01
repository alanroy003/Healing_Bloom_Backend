from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger Schema View
schema_view = get_schema_view(
    openapi.Info(
        title="Healing Bloom API",
        default_version="v1",
        description="API documentation for the Healing Bloom project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@healingbloom.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
) 