from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import QuoteForm

def home(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your quote request has been submitted. We will contact you shortly.')
            return redirect('home')
    else:
        form = QuoteForm()

    testimonials = [
        {"quote": "Quickly fixed the issue. Very polite and respectful of my time. Excellent service!", "name": "Aryan Subedi", "title": "CEO"},
        {"quote": "Professional, Quick response, Excellent service, Dedicated team! All you need in a great business.", "name": "Perry Andrews", "title": "SWIFT Inc."},
        {"quote": "Very reliable IT Company, efficient in their work. Staff are very co-operative and accommodating.", "name": "Sammy Browns", "title": "CFO, Perfect Inc."},
    ]

    return render(request, 'core/home.html', {'form': form, 'testimonials': testimonials})

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! We will get back to you shortly.')
            return redirect('contact')
    else:
        form = QuoteForm()
    return render(request, 'core/contact.html', {'form': form})


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import anthropic

SYSTEM_PROMPT = """You are Aria, a friendly and knowledgeable AI assistant for Spread International — a premium IT solution provider based in Dubai, UAE.

Your job is to help website visitors with questions about our services, pricing, support, and general IT topics.

== ABOUT SPREAD INTERNATIONAL ==
- Company: Spread International (also known as Spread Technical)
- Location: Bur Dubai, U.A.E.
- Phone: +971-528269410
- Email: it@spreadtechnical.com
- WhatsApp: +971528269410

== OUR SERVICES ==

IT Solutions:
- IT Hardware & Network Services
- Annual Maintenance Contract (AMC) — starting AED 1999/year
- Server, Computer, Laptop sales & services
- Network/Security solutions (firewalls, VPNs, etc.)
- Structured Cabling
- IP Camera / CCTV Solutions
- Backup Solutions
- Antivirus Solutions
- Telephone PABX Solution (Panasonic)

Digital Marketing:
- Web Development
- Graphics Designing
- Mobile Apps Development
- Digital Marketing (SEO, Social Media, Email)

VAT / Tax Related IT Solutions:
- VAT/Tax Consultation
- VAT Registration
- VAT Consultancy and Impact Assessment
- VAT Implementation and Training
- VAT Accounting and Compliance
- Filing of VAT Returns

== TONE & RULES ==
- Be warm, professional, and concise.
- Keep responses short (2-4 sentences max unless a detailed answer is needed).
- If asked for a quote or pricing, encourage them to fill in the Free Quote form or call us.
- If you don't know something specific, say you'll connect them with our team.
- Never make up prices (except AMC which starts at AED 1999).
- Always end with a helpful follow-up offer if appropriate.
- Use bullet points for lists to keep things readable.
"""

@csrf_exempt
@require_POST
def chatbot(request):
    try:
        data = json.loads(request.body)
        messages = data.get('messages', [])

        if not messages:
            return JsonResponse({'error': 'No messages provided'}, status=400)

        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            system=SYSTEM_PROMPT,
            messages=messages
        )

        reply = response.content[0].text
        return JsonResponse({'reply': reply})

    except Exception as e:
        return JsonResponse({'reply': "I'm sorry, I'm having a bit of trouble right now. Please call us at +971-528269410 or email it@spreadtechnical.com for immediate help!"})
