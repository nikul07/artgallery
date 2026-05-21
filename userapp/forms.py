from django import forms
from userapp import models
from userapp.models import ContactMessage

class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = models.BillingAddress
        fields = "__all__"
        exclude = ['final']

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone_number', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email Address'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Your Phone Number'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message'}),
        } 