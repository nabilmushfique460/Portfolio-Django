import csv
import logging
from pathlib import Path
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import ContactForm

logger = logging.getLogger(__name__)

# Curated free Unsplash images and category metadata for data.csv projects
PROJECT_METADATA = {
    "1.png": {
        "image_url": "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?auto=format&fit=crop&w=1200&q=80",
        "category": "Web Application",
        "category_slug": "web",
        "badge": "Django & Python",
        "tags": ["Django", "Python", "Full-Stack", "Task Flow"],
        "featured": True,
    },
    "2.png": {
        "image_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80",
        "category": "Web Application",
        "category_slug": "web",
        "badge": "Full-Stack Python",
        "tags": ["Python", "Vanilla JS", "Responsive UI"],
        "featured": False,
    },
    "3.png": {
        "image_url": "https://images.unsplash.com/photo-1586281380349-632531db7ed4?auto=format&fit=crop&w=1200&q=80",
        "category": "Automation",
        "category_slug": "automation",
        "badge": "PDF Automation",
        "tags": ["Python", "PDF Generator", "Document Engine"],
        "featured": False,
    },
    "4.png": {
        "image_url": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=1200&q=80",
        "category": "Automation",
        "category_slug": "automation",
        "badge": "Excel & PDF Engine",
        "tags": ["OpenPyXL", "PDF Toolkit", "ETL Process"],
        "featured": False,
    },
    "5.png": {
        "image_url": "https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=1200&q=80",
        "category": "AI & Data",
        "category_slug": "ai-data",
        "badge": "Sentiment NLP",
        "tags": ["NLP Engine", "News API", "Sentiment AI"],
        "featured": False,
    },
    "6.png": {
        "image_url": "https://images.unsplash.com/photo-1592210454359-9043f067919b?auto=format&fit=crop&w=1200&q=80",
        "category": "REST API",
        "category_slug": "api",
        "badge": "Flask Microservice",
        "tags": ["Flask", "RESTful API", "JSON Feed"],
        "featured": False,
    },
    "7.png": {
        "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=80",
        "category": "Web Application",
        "category_slug": "web",
        "badge": "Booking Engine",
        "tags": ["Python", "Booking Architecture", "UX Flow"],
        "featured": True,
    },
    "8.png": {
        "image_url": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=1200&q=80",
        "category": "Automation",
        "category_slug": "automation",
        "badge": "Web Scraping",
        "tags": ["BeautifulSoup", "SMTP Mailer", "Event Monitor"],
        "featured": False,
    },
    "9.png": {
        "image_url": "https://images.unsplash.com/photo-1531746790731-6c087fecd65a?auto=format&fit=crop&w=1200&q=80",
        "category": "AI & Data",
        "category_slug": "ai-data",
        "badge": "Domain Assistant",
        "tags": ["Knowledge Base", "AI Agent", "NLP Queries"],
        "featured": False,
    },
    "10.png": {
        "image_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1200&q=80",
        "category": "AI & Data",
        "category_slug": "ai-data",
        "badge": "Conversational AI",
        "tags": ["Facebook API", "NLP Engine", "Chat Gateway"],
        "featured": False,
    },
    "11.png": {
        "image_url": "https://images.unsplash.com/photo-1557597774-9d273605dfa9?auto=format&fit=crop&w=1200&q=80",
        "category": "AI & Data",
        "category_slug": "ai-data",
        "badge": "Computer Vision",
        "tags": ["OpenCV", "Motion Detection", "Email Trigger"],
        "featured": False,
    },
    "12.png": {
        "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=1200&q=80",
        "category": "Analytics",
        "category_slug": "analytics",
        "badge": "Keystroke Analytics",
        "tags": ["Keyboard Hook", "Word Analytics", "Stats Daemon"],
        "featured": False,
    },
    "13.png": {
        "image_url": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&w=1200&q=80",
        "category": "Analytics",
        "category_slug": "analytics",
        "badge": "Network Telemetry",
        "tags": ["Network Telemetry", "Real-Time Graph", "Web Plotter"],
        "featured": False,
    },
    "14.png": {
        "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80",
        "category": "Analytics",
        "category_slug": "analytics",
        "badge": "Monitoring Daemon",
        "tags": ["Remote Server", "Cron Monitor", "Health Check"],
        "featured": False,
    },
    "15.png": {
        "image_url": "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=1200&q=80",
        "category": "Analytics",
        "category_slug": "analytics",
        "badge": "Data Visualization",
        "tags": ["Matplotlib", "Data Pipeline", "Visual Analytics"],
        "featured": False,
    },
    "16.png": {
        "image_url": "https://images.unsplash.com/photo-1534088568595-a066f410bcda?auto=format&fit=crop&w=1200&q=80",
        "category": "Analytics",
        "category_slug": "analytics",
        "badge": "Weather Dashboard",
        "tags": ["5-Day Forecast", "Data Charts", "API Client"],
        "featured": False,
    },
    "17.png": {
        "image_url": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1200&q=80",
        "category": "Desktop GUI",
        "category_slug": "desktop",
        "badge": "PyQt6 & SQL",
        "tags": ["PyQt6 Desktop", "SQLite DB", "Admin Dashboard"],
        "featured": False,
    },
    "18.png": {
        "image_url": "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=1200&q=80",
        "category": "Desktop GUI",
        "category_slug": "desktop",
        "badge": "PyQt6 & SQL",
        "tags": ["PyQt6 Desktop", "Relational SQL", "Academic Ops"],
        "featured": False,
    },
    "19.png": {
        "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
        "category": "Web Application",
        "category_slug": "web",
        "badge": "Django Web App",
        "tags": ["Django", "Real-Time Menu", "Dynamic Filters"],
        "featured": True,
    },
    "20.png": {
        "image_url": "https://images.unsplash.com/photo-1472851294608-062f824d29cc?auto=format&fit=crop&w=1200&q=80",
        "category": "Web Application",
        "category_slug": "web",
        "badge": "Django E-Commerce",
        "tags": ["Django E-Commerce", "Order Processing", "Seller Portal"],
        "featured": True,
    },
}


def load_projects_from_csv():
    """Reads projects from data.csv and attaches rich metadata and free image URLs."""
    csv_path = settings.BASE_DIR / 'data.csv'
    projects = []
    fallback_image = "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80"

    if not csv_path.exists():
        return projects

    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for index, row in enumerate(reader, start=1):
                img_key = row.get('image', f'{index}.png').strip()
                meta = PROJECT_METADATA.get(img_key, {})
                img_url = meta.get('image_url', fallback_image)
                category = meta.get('category', 'Software')
                category_slug = meta.get('category_slug', 'all')
                badge = meta.get('badge', 'Python')
                tags = meta.get('tags', ['Python', category])
                featured = meta.get('featured', False)

                raw_url = row.get('url', '').strip()
                # Clean up repo link if it had a placeholder suffix
                if raw_url.endswith('.png'):
                    repo_url = 'https://github.com/nabilmushfique460'
                else:
                    repo_url = raw_url

                projects.append({
                    'id': index,
                    'title': row.get('title', '').strip(),
                    'description': row.get('description', '').strip(),
                    'url': repo_url,
                    'image': img_url,
                    'category': category,
                    'category_slug': category_slug,
                    'badge': badge,
                    'tags': tags,
                    'featured': featured,
                })
    except Exception as e:
        logger.error("Error reading data.csv: %s", e)

    return projects


def home(request):
    """Show the Home page (hero section + services overview)."""
    return render(request, 'home.html')


def about(request):
    """Show the Projects (About) page."""
    projects = load_projects_from_csv()
    return render(request, 'about.html', {'projects': projects})


def services(request):
    """Show the Services page (service list lives in the template)."""
    return render(request, 'services.html')


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
            admin_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'nabil29089@gmail.com')

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
                    from_email=admin_email,
                    recipient_list=[email],
                    fail_silently=False,
                )
                # Send notification email to admin
                send_mail(
                    subject=admin_subject,
                    message=admin_body,
                    from_email=admin_email,
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


