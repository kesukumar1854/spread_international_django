from django import forms
from .models import QuoteRequest

class QuoteForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ['name', 'company', 'email', 'phone', 'service', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name *', 'required': True}),
            'company': forms.TextInput(attrs={'placeholder': 'Company Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address *', 'required': True}),
            'phone': forms.TextInput(attrs={'placeholder': 'Contact Number *', 'required': True}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message', 'rows': 4}),
        }
