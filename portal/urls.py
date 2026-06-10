from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('',                     views.app_shell,           name='app'),
    path('login/',               views.app_login,            name='login'),
    path('register/',            views.app_register,         name='register'),
    path('logout/',              views.app_logout,            name='logout'),

    # API
    path('api/me/',              views.api_me,               name='api_me'),
    path('api/me/update/',       views.api_update_profile,   name='api_update_profile'),
    path('api/dashboard/',       views.api_dashboard,        name='api_dashboard'),
    path('api/bookings/',        views.api_bookings,         name='api_bookings'),
    path('api/bookings/<int:pk>/cancel/', views.api_cancel_booking, name='api_cancel_booking'),
    path('api/tickets/',         views.api_tickets,          name='api_tickets'),
    path('api/tickets/<int:pk>/',views.api_ticket_detail,    name='api_ticket_detail'),
    path('api/notifications/',   views.api_notifications,    name='api_notifications'),
    path('api/services/',        views.api_services,         name='api_services'),
    path('api/ai-chat/',         views.api_ai_chat,          name='api_ai_chat'),
]
