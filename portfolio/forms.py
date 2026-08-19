# Forms for the portfolio app.
#
# ContactForm is a Django ModelForm tied to the ContactMessage model.
# It handles form validation and allows saving submissions directly to the database.

from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        labels = {
            'name': 'Your Name',
            'email': 'Your Email',
            'message': 'Message',
        }
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }

