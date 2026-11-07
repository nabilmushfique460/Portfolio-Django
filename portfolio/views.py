import logging
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import ContactForm
from .models import Project, Service

logger = logging.getLogger(__name__)


def home(request):
    """Show the Home page (hero section + services overview)."""
    return render(request, 'home.html')


def about(request):
    """Show the Projects (About) page — data is pulled from the database."""
    projects = Project.objects.all()

    # Build template-friendly dicts that match what about.html expects.
    project_list = []
    for idx, p in enumerate(projects, start=1):
        project_list.append({
            'id': idx,
            'title': p.title,
            'description': p.description,
            'url': p.url,
            'image': p.display_image,
            'category': p.category,
            'category_slug': p.category_slug,
            'badge': p.badge,
            'tags': p.tags_list,
            'featured': p.featured,
        })

    # Build dynamic category counts for the filter pills.
    categories = {}
    for proj in project_list:
        slug = proj['category_slug']
        categories[slug] = categories.get(slug, 0) + 1

    return render(request, 'about.html', {
        'projects': project_list,
        'categories': categories,
        'total_count': len(project_list),
    })


def services(request):
    """Show the Services / Offerings page — data is pulled from the database."""
    service_qs = Service.objects.all()

    service_list = []
    for idx, s in enumerate(service_qs, start=1):
        service_list.append({
            'id': f'{idx:02d}',
            'title': s.title,
            'category': s.category,
            'description': s.description,
            'deliverables': s.deliverables_list,
            'tags': s.tags_list,
            'image': s.display_image,
            'badge': s.badge,
        })

    return render(request, 'services.html', {'services': service_list})


def contact(request):
    """
    Show the Contact page.

    - On a normal visit (GET request), show an empty ContactForm.
    - On a form submission (POST request), validate the data. If it's
      valid, save the message to db.sqlite3, send a confirmation email
      to the sender and a notification email to the admin, and flag success=True
      so the template can show a "Thank you" message. If it's invalid,
      Django automatically re-shows the form with error messages next to each field.
    """
    success = False

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
            except Exception as e:
                logger.error("Failed to send contact email: %s", e)

            success = True
            form = ContactForm()  # reset to a blank form after success
    else:
        form = ContactForm()

    context = {
        'form': form,
        'success': success,
    }
    return render(request, 'contact.html', context)
