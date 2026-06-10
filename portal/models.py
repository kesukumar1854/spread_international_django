from django.db import models
from django.contrib.auth.models import User

SERVICES = [
    ('amc',           'Annual Maintenance Contract (AMC)'),
    ('network',       'Network Setup / Issues'),
    ('ipcamera',      'IP Camera / CCTV'),
    ('pabx',          'Telephone PABX Solution'),
    ('webdev',        'Web Development'),
    ('social',        'Social Media Marketing'),
    ('apps',          'Mobile Apps Development'),
    ('vat_consult',   'VAT/Tax Consultation'),
    ('vat_reg',       'VAT Registration'),
    ('vat_compliance','VAT Accounting & Compliance'),
    ('vat_returns',   'Filing of VAT Returns'),
    ('others',        'Others'),
]

class ClientProfile(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    company    = models.CharField(max_length=200, blank=True)
    phone      = models.CharField(max_length=50, blank=True)
    address    = models.TextField(blank=True)
    avatar     = models.CharField(max_length=10, default='👤')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"


class Booking(models.Model):
    STATUS = [
        ('pending',    'Pending'),
        ('confirmed',  'Confirmed'),
        ('inprogress', 'In Progress'),
        ('completed',  'Completed'),
        ('cancelled',  'Cancelled'),
    ]
    client         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    service        = models.CharField(max_length=50, choices=SERVICES)
    description    = models.TextField()
    preferred_date = models.DateField(null=True, blank=True)
    preferred_time = models.TimeField(null=True, blank=True)
    status         = models.CharField(max_length=20, choices=STATUS, default='pending')
    notes          = models.TextField(blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client.username} - {self.get_service_display()} [{self.status}]"

    class Meta:
        ordering = ['-created_at']


class SupportTicket(models.Model):
    PRIORITY = [('low','Low'),('medium','Medium'),('high','High'),('urgent','Urgent')]
    STATUS   = [('open','Open'),('inprogress','In Progress'),('resolved','Resolved'),('closed','Closed')]

    client     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    subject    = models.CharField(max_length=300)
    category   = models.CharField(max_length=50, choices=SERVICES)
    priority   = models.CharField(max_length=10, choices=PRIORITY, default='medium')
    status     = models.CharField(max_length=20, choices=STATUS, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.pk} {self.subject} [{self.status}]"

    class Meta:
        ordering = ['-created_at']


class TicketMessage(models.Model):
    ticket     = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='messages')
    sender     = models.ForeignKey(User, on_delete=models.CASCADE)
    is_staff   = models.BooleanField(default=False)
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class Notification(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title      = models.CharField(max_length=200)
    body       = models.TextField()
    icon       = models.CharField(max_length=10, default='🔔')
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
