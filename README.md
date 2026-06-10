# Spread International - Django Website

A complete Django replica of spreadtechnical.com.

## Features
- Responsive homepage with hero slider, services, process steps, testimonials, blog section
- Quote request form with database storage
- About Us & Contact pages
- Django Admin panel for managing quote requests
- WhatsApp floating button

## Setup & Run

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. (Optional) Create admin superuser
python manage.py createsuperuser

# 5. Run development server
python manage.py runserver
```

Visit: http://127.0.0.1:8000/
Admin: http://127.0.0.1:8000/admin/

## Project Structure
```
spread_international/
├── core/                   # Main app
│   ├── templates/core/     # HTML templates
│   ├── static/css/         # Stylesheets
│   ├── templatetags/       # Custom filters
│   ├── models.py           # QuoteRequest model
│   ├── views.py            # Home, About, Contact views
│   ├── forms.py            # QuoteForm
│   ├── admin.py            # Admin registration
│   └── urls.py             # App URL patterns
├── spread_international/   # Project config
│   ├── settings.py
│   └── urls.py
├── requirements.txt
└── manage.py
```
