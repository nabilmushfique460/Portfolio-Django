import logging
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ContactForm
from .models import Project, Service

logger = logging.getLogger(__name__)


def home(request):
    """Show the Home page (hero section + services overview)."""
    return render(request, 'home.html')


def about(request):
    """Show the Projects (About) page — data is pulled from the database."""
    projects = Project.objects.all()

    # Build dynamic category counts using ORM aggregation
    cat_counts = (
        Project.objects.values('category_slug')
        .annotate(total=Count('id'))
        .order_by('category_slug')
    )
    categories = {item['category_slug']: item['total'] for item in cat_counts}

    return render(request, 'about.html', {
        'projects': projects,
        'categories': categories,
        'total_count': projects.count(),
    })


def services(request):
    """Show the Services / Offerings page — data is pulled from the database."""
    service_qs = Service.objects.all()
    return render(request, 'services.html', {'services': service_qs})


def contact(request):
    """
    Show the Contact page.

    - On GET: renders empty ContactForm, checking for 'status' query param from PRG redirect.
    - On POST: validates form (including anti-bot honeypot). If valid, saves message,
      dispatches confirmation and notification emails, and redirects (PRG pattern).
    """
    status = request.GET.get('status')
    success = (status == 'success')
    saved_delivery_failed = (status == 'saved_delivery_failed')

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()

            # Email details
            name = contact_message.name
            email = contact_message.email
            message = contact_message.message
            default_from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'nabil29089@gmail.com')
            admin_email = getattr(settings, 'ADMIN_EMAIL', default_from_email)

            # 1. Confirmation email to the person submitting the form
            user_subject = "Thank you for getting in touch!"
            user_body = (
                f"Hi {name},\n\n"
                f"Thank you for contacting me. I have received your message and will get back to you as soon as possible.\n\n"
                f"Your Submitted Message:\n"
                f"{message}\n\n"
                f"Best regards,\n"
                f"S.M. Nabil Mushfique"
            )

            # 2. Notification email to the admin with all details (Name, Email, Message)
            admin_subject = f"New Contact Message from {name}"
            admin_body = (
                f"You have received a new contact form submission on your website:\n\n"
                f"Name: {name}\n"
                f"Email: {email}\n\n"
                f"Message:\n"
                f"{message}\n"
            )

            email_sent = False
            try:
                # Send confirmation email to user
                send_mail(
                    subject=user_subject,
                    message=user_body,
                    from_email=default_from_email,
                    recipient_list=[email],
                    fail_silently=False,
                )
                # Send notification email to admin
                send_mail(
                    subject=admin_subject,
                    message=admin_body,
                    from_email=default_from_email,
                    recipient_list=[admin_email],
                    fail_silently=False,
                )
                email_sent = True
            except Exception as e:
                logger.error("Failed to send contact email: %s", e)

            # Post/Redirect/Get pattern: redirect to GET with status param
            target_status = 'success' if email_sent else 'saved_delivery_failed'
            return redirect(f"{reverse('contact')}?status={target_status}")
    else:
        form = ContactForm()

    context = {
        'form': form,
        'success': success,
        'saved_delivery_failed': saved_delivery_failed,
    }
    return render(request, 'contact.html', context)
