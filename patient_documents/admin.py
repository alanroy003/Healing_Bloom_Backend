from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_type', 'upload_date', 'updated_at')
    list_filter = ('document_type', 'upload_date')
    search_fields = ('user__email', 'notes')
    readonly_fields = ('upload_date', 'updated_at')