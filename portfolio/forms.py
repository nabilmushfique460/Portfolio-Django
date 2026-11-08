from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Hidden honeypot field for anti-bot spam protection
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
            'tabindex': '-1',
            'style': 'display:none !important;',
            'aria-hidden': 'true',
        }),
    )

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

    def clean(self):
        cleaned_data = super().clean()
        # If the hidden honeypot field is populated, reject the submission as bot spam
        if cleaned_data.get('website'):
            raise forms.ValidationError("Spam detected.")
        return cleaned_data
