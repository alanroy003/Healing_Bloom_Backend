# HealingBloom_Backend\patient_documents\views.py
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer ,  EmptySerializer
from accounts.models import CustomUser
from django.http import FileResponse
from rest_framework.views import APIView 


class DocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Document.objects.none()

        return Document.objects.filter(user=self.request.user).select_related('user')

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response(
                {'error': 'Authentication credentials were not provided.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return super().handle_exception(exc)

class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Document.objects.none()
        return Document.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except NotFound:
            return Response(
                {'error': 'Document not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def perform_destroy(self, instance):
        try:
            instance.file.delete()  # Delete the actual file
            instance.delete()
        except Exception as e:
            return Response(
                {'error': f'Error deleting document: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def handle_exception(self, exc):
        if isinstance(exc, NotFound):
            return Response(
                {'error': 'Document not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        return super().handle_exception(exc)

class DocumentDownloadView(APIView):  
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmptySerializer

    def get(self, request, *args, **kwargs):
        try:
            document = Document.objects.get(id=kwargs['id'], user=request.user)
            file_path = document.file.path
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{document.filename()}"'
            return response
        except Document.DoesNotExist:
            return Response(
                {'error': 'Document not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error downloading document: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )