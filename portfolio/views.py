# Views for the portfolio app.
#
# A "view" is just a Python function that takes a web request and
# returns a web response. Here, home/about/services simply render
# (display) their template with no extra data. The contact view is
# slightly more involved because it needs to handle a submitted form.

from django.shortcuts import render
from .forms import ContactForm


def home(request):
    """Show the Home page (hero section + services overview)."""
    return render(request, 'home.html')


def about(request):
    """Show the About page."""
    return render(request, 'about.html')


def services(request):
    """Show the Services page (service list lives in the template)."""
    return render(request, 'services.html')


def contact(request):
    """
    Show the Contact page.

    - On a normal visit (GET request), show an empty ContactForm.
    - On a form submission (POST request), validate the data. If it's
      valid, we don't email it or save it anywhere (as requested) -
      we just flag success=True so the template can show a
      "Thank you" message. If it's invalid, Django automatically
      re-shows the form with error messages next to each field.
    """
    success = False

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            success = True
            form = ContactForm()  # reset to a blank form after success
    else:
        form = ContactForm()

    context = {
        'form': form,
        'success': success,
    }
    return render(request, 'contact.html', context)
