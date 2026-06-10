from django.contrib import admin
from .models import ClientProfile, Booking, SupportTicket, TicketMessage, Notification

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ['user','company','phone','created_at']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['client','service','status','preferred_date','created_at']
    list_filter  = ['status','service']

class TicketMessageInline(admin.TabularInline):
    model = TicketMessage
    extra = 1

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['id','client','subject','category','priority','status','created_at']
    list_filter  = ['status','priority','category']
    inlines      = [TicketMessageInline]

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user','title','is_read','created_at']
