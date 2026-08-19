# Forms for the portfolio app.
#
# ContactForm is a plain Django "forms.Form" (not tied to a database
# model). It simply describes which fields the contact form has and
# how each one should be validated.

from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Your Name",
    )
    email = forms.EmailField(
        label="Your Email",
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={'rows': 5}),
    )
