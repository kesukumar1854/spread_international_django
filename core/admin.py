from django.contrib import admin
from .models import QuoteRequest

@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'email', 'phone', 'service', 'created_at']
    list_filter = ['service', 'created_at']
    search_fields = ['name', 'email', 'company']
