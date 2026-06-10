import json
import anthropic
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import ClientProfile, Booking, SupportTicket, TicketMessage, Notification, SERVICES

# ── helpers ──────────────────────────────────────────────────────────────────
def make_notification(user, title, body, icon='🔔'):
    Notification.objects.create(user=user, title=title, body=body, icon=icon)

# ── auth ──────────────────────────────────────────────────────────────────────
def app_login(request):
    if request.user.is_authenticated:
        return redirect('portal:dashboard')
    error = ''
    if request.method == 'POST':
        d = json.loads(request.body)
        u = authenticate(request, username=d.get('username'), password=d.get('password'))
        if u:
            login(request, u)
            return JsonResponse({'ok': True})
        error = 'Invalid username or password'
    if request.method == 'GET':
        return render(request, 'portal/app.html')
    return JsonResponse({'ok': False, 'error': error}, status=401)

def app_register(request):
    if request.method == 'POST':
        d = json.loads(request.body)
        username = d.get('username','').strip()
        email    = d.get('email','').strip()
        password = d.get('password','')
        name     = d.get('name','').strip()
        company  = d.get('company','').strip()
        phone    = d.get('phone','').strip()
        if User.objects.filter(username=username).exists():
            return JsonResponse({'ok': False, 'error': 'Username already taken'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'ok': False, 'error': 'Email already registered'}, status=400)
        u = User.objects.create_user(username=username, email=email, password=password)
        parts = name.split(' ', 1)
        u.first_name = parts[0]
        u.last_name  = parts[1] if len(parts) > 1 else ''
        u.save()
        ClientProfile.objects.create(user=u, company=company, phone=phone)
        login(request, u)
        make_notification(u, 'Welcome to Spread International! 🎉',
                          'Your account is ready. Explore our services and book your first appointment.', '🎉')
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=405)

@login_required
def app_logout(request):
    logout(request)
    return redirect('portal:app')

# ── API: user info ────────────────────────────────────────────────────────────
@login_required
def api_me(request):
    u = request.user
    profile, _ = ClientProfile.objects.get_or_create(user=u)
    unread = Notification.objects.filter(user=u, is_read=False).count()
    return JsonResponse({
        'id': u.id,
        'username': u.username,
        'name': u.get_full_name() or u.username,
        'email': u.email,
        'company': profile.company,
        'phone': profile.phone,
        'address': profile.address,
        'avatar': profile.avatar,
        'unread_notifications': unread,
        'member_since': u.date_joined.strftime('%b %Y'),
    })

@login_required
@require_POST
def api_update_profile(request):
    d = json.loads(request.body)
    u = request.user
    profile, _ = ClientProfile.objects.get_or_create(user=u)
    name = d.get('name','').strip()
    parts = name.split(' ', 1)
    u.first_name = parts[0]
    u.last_name  = parts[1] if len(parts) > 1 else ''
    u.email = d.get('email', u.email)
    u.save()
    profile.company = d.get('company', profile.company)
    profile.phone   = d.get('phone', profile.phone)
    profile.address = d.get('address', profile.address)
    profile.save()
    return JsonResponse({'ok': True})

# ── API: dashboard ────────────────────────────────────────────────────────────
@login_required
def api_dashboard(request):
    u = request.user
    bookings = Booking.objects.filter(client=u)
    tickets  = SupportTicket.objects.filter(client=u)
    return JsonResponse({
        'stats': {
            'total_bookings':    bookings.count(),
            'active_bookings':   bookings.filter(status__in=['pending','confirmed','inprogress']).count(),
            'open_tickets':      tickets.filter(status__in=['open','inprogress']).count(),
            'resolved_tickets':  tickets.filter(status='resolved').count(),
        },
        'recent_bookings': [
            {'id': b.id, 'service': b.get_service_display(),
             'status': b.status, 'date': b.created_at.strftime('%d %b %Y')}
            for b in bookings[:4]
        ],
        'recent_tickets': [
            {'id': t.id, 'subject': t.subject,
             'status': t.status, 'priority': t.priority,
             'date': t.created_at.strftime('%d %b %Y')}
            for t in tickets[:4]
        ],
    })

# ── API: bookings ─────────────────────────────────────────────────────────────
@login_required
def api_bookings(request):
    if request.method == 'GET':
        bks = Booking.objects.filter(client=request.user)
        return JsonResponse({'bookings': [
            {'id': b.id, 'service': b.get_service_display(),
             'service_key': b.service,
             'description': b.description,
             'preferred_date': str(b.preferred_date) if b.preferred_date else '',
             'preferred_time': str(b.preferred_time) if b.preferred_time else '',
             'status': b.status, 'notes': b.notes,
             'created_at': b.created_at.strftime('%d %b %Y')}
            for b in bks
        ]})
    if request.method == 'POST':
        d = json.loads(request.body)
        b = Booking.objects.create(
            client=request.user,
            service=d.get('service'),
            description=d.get('description',''),
            preferred_date=d.get('preferred_date') or None,
            preferred_time=d.get('preferred_time') or None,
        )
        make_notification(request.user,
            f'Booking #{b.id} Received ✅',
            f'Your booking for {b.get_service_display()} has been received. We will confirm shortly.', '📅')
        return JsonResponse({'ok': True, 'id': b.id})

@login_required
@require_POST
def api_cancel_booking(request, pk):
    b = get_object_or_404(Booking, pk=pk, client=request.user)
    if b.status in ('pending','confirmed'):
        b.status = 'cancelled'
        b.save()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False, 'error': 'Cannot cancel at this stage'}, status=400)

# ── API: tickets ──────────────────────────────────────────────────────────────
@login_required
def api_tickets(request):
    if request.method == 'GET':
        tks = SupportTicket.objects.filter(client=request.user)
        return JsonResponse({'tickets': [
            {'id': t.id, 'subject': t.subject, 'category': t.get_category_display(),
             'priority': t.priority, 'status': t.status,
             'created_at': t.created_at.strftime('%d %b %Y'),
             'msg_count': t.messages.count()}
            for t in tks
        ]})
    if request.method == 'POST':
        d = json.loads(request.body)
        t = SupportTicket.objects.create(
            client=request.user,
            subject=d.get('subject',''),
            category=d.get('category','others'),
            priority=d.get('priority','medium'),
        )
        TicketMessage.objects.create(
            ticket=t, sender=request.user,
            message=d.get('message','(no description)')
        )
        make_notification(request.user,
            f'Ticket #{t.id} Created 🎫',
            f'Support ticket "{t.subject}" has been created. Our team will respond within 24 hours.', '🎫')
        return JsonResponse({'ok': True, 'id': t.id})

@login_required
def api_ticket_detail(request, pk):
    t = get_object_or_404(SupportTicket, pk=pk, client=request.user)
    if request.method == 'GET':
        return JsonResponse({
            'id': t.id, 'subject': t.subject,
            'category': t.get_category_display(),
            'priority': t.priority, 'status': t.status,
            'created_at': t.created_at.strftime('%d %b %Y %H:%M'),
            'messages': [
                {'sender': m.sender.get_full_name() or m.sender.username,
                 'is_staff': m.is_staff,
                 'message': m.message,
                 'time': m.created_at.strftime('%d %b %H:%M')}
                for m in t.messages.all()
            ]
        })
    if request.method == 'POST':
        d = json.loads(request.body)
        TicketMessage.objects.create(
            ticket=t, sender=request.user, message=d.get('message',''))
        t.status = 'inprogress'
        t.save()
        return JsonResponse({'ok': True})

# ── API: notifications ────────────────────────────────────────────────────────
@login_required
def api_notifications(request):
    notes = Notification.objects.filter(user=request.user)
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'notifications': [
        {'id': n.id, 'title': n.title, 'body': n.body,
         'icon': n.icon, 'is_read': n.is_read,
         'time': n.created_at.strftime('%d %b %H:%M')}
        for n in notes
    ]})

# ── API: services list ────────────────────────────────────────────────────────
@login_required
def api_services(request):
    return JsonResponse({'services': [{'key': k, 'label': v} for k, v in SERVICES]})

# ── AI chat (app) ─────────────────────────────────────────────────────────────
APP_AI_PROMPT = """You are Aria, the intelligent AI assistant embedded inside the Spread International Client Portal App.

You help authenticated clients with:
- Understanding their bookings and ticket statuses
- Recommending services based on their needs
- Providing IT support guidance and troubleshooting tips
- Answering questions about VAT, networking, web development, CCTV, etc.
- Navigating the app features

== SPREAD INTERNATIONAL SERVICES ==
IT: Hardware & Network, AMC (from AED 1999/yr), IP Camera/CCTV, PABX, Cabling, Backup, Antivirus
Digital: Web Dev, Mobile Apps, SEO, Social Media, Graphics
VAT: Registration, Consultation, Compliance, Returns Filing

Contact: +971-528269410 | it@spreadtechnical.com | Bur Dubai, UAE

== TONE ==
Be warm, concise, and helpful. Use bullet points for lists.
If you don't know something specific, offer to connect them with the team.
Keep responses under 120 words unless a technical explanation is needed.
"""

@login_required
@csrf_exempt
@require_POST
def api_ai_chat(request):
    try:
        d = json.loads(request.body)
        messages = d.get('messages', [])
        client = anthropic.Anthropic()
        resp = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=400,
            system=APP_AI_PROMPT,
            messages=messages
        )
        return JsonResponse({'reply': resp.content[0].text})
    except Exception as e:
        return JsonResponse({'reply': "I'm having trouble right now. Please call +971-528269410 for immediate support."})

# ── main app shell ────────────────────────────────────────────────────────────
def app_shell(request):
    return render(request, 'portal/app.html')
