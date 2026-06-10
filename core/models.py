from django.db import models

class QuoteRequest(models.Model):
    SERVICES = [
        ('amc', 'Annual Maintenance Contract (AMC)'),
        ('network', 'Network Setup / Issues'),
        ('ipcamera', 'IP Camera'),
        ('pabx', 'Telephone PABX Solution'),
        ('webdev', 'Web Development'),
        ('social', 'Social Media Marketing'),
        ('apps', 'Apps Development'),
        ('vat_consult', 'VAT/Tax Consultation'),
        ('vat_reg', 'VAT Registration'),
        ('vat_impact', 'VAT Consultancy and Impact Assessment'),
        ('vat_training', 'VAT Implementation and Training'),
        ('vat_compliance', 'VAT Accounting and Compliance'),
        ('vat_returns', 'Filing of VAT Returns'),
        ('others', 'Others'),
    ]
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    service = models.CharField(max_length=50, choices=SERVICES)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_service_display()}"
