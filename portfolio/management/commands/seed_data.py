"""
Management command to import existing hardcoded projects and services
into the database, making them editable from Django admin.

Usage:  python manage.py seed_data
"""
import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from portfolio.models import Project, Service


# Curated metadata (from the original views.py PROJECT_METADATA)
PROJECT_METADATA = {
    "1.png": {
        "image_url": "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?auto=format&fit=crop&w=1200&q=80",
        "category": "Web Application", "category_slug": "web",
        "badge": "Django & Python",
        "tags": "Django, Python, Full-Stack, Task Flow",
        "featured": True,
    },
    "2.png": {
        "image_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80",
        "category": "Web Application", "category_slug": "web",
        "badge": "Full-Stack Python",
        "tags": "Python, Vanilla JS, Responsive UI",
        "featured": False,
    },
    "3.png": {
        "image_url": "https://images.unsplash.com/photo-1586281380349-632531db7ed4?auto=format&fit=crop&w=1200&q=80",
        "category": "Automation", "category_slug": "automation",
        "badge": "PDF Automation",
        "tags": "Python, PDF Generator, Document Engine",
        "featured": False,
    },
    "4.png": {
        "image_url": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=1200&q=80",
        "category": "Automation", "category_slug": "automation",
        "badge": "Excel & PDF Engine",
        "tags": "OpenPyXL, PDF Toolkit, ETL Process",
        "featured": False,
    },
    "5.png": {
        "image_url": "https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=1200&q=80",
        "category": "AI & Data", "category_slug": "ai-data",
        "badge": "Sentiment NLP",
        "tags": "NLP Engine, News API, Sentiment AI",
        "featured": False,
    },
    "6.png": {
        "image_url": "https://images.unsplash.com/photo-1592210454359-9043f067919b?auto=format&fit=crop&w=1200&q=80",
        "category": "REST API", "category_slug": "api",
        "badge": "Flask Microservice",
        "tags": "Flask, RESTful API, JSON Feed",
        "featured": False,
    },
    "7.png": {
        "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=80",
        "category": "Web Application", "category_slug": "web",
        "badge": "Booking Engine",
        "tags": "Python, Booking Architecture, UX Flow",
        "featured": True,
    },
    "8.png": {
        "image_url": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=1200&q=80",
        "category": "Automation", "category_slug": "automation",
        "badge": "Web Scraping",
        "tags": "BeautifulSoup, SMTP Mailer, Event Monitor",
        "featured": False,
    },
    "9.png": {
        "image_url": "https://images.unsplash.com/photo-1531746790731-6c087fecd65a?auto=format&fit=crop&w=1200&q=80",
        "category": "AI & Data", "category_slug": "ai-data",
        "badge": "Domain Assistant",
        "tags": "Knowledge Base, AI Agent, NLP Queries",
        "featured": False,
    },
    "10.png": {
        "image_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1200&q=80",
        "category": "AI & Data", "category_slug": "ai-data",
        "badge": "Conversational AI",
        "tags": "Facebook API, NLP Engine, Chat Gateway",
        "featured": False,
    },
    "11.png": {
        "image_url": "https://images.unsplash.com/photo-1557597774-9d273605dfa9?auto=format&fit=crop&w=1200&q=80",
        "category": "AI & Data", "category_slug": "ai-data",
        "badge": "Computer Vision",
        "tags": "OpenCV, Motion Detection, Email Trigger",
        "featured": False,
    },
    "12.png": {
        "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=1200&q=80",
        "category": "Analytics", "category_slug": "analytics",
        "badge": "Keystroke Analytics",
        "tags": "Keyboard Hook, Word Analytics, Stats Daemon",
        "featured": False,
    },
    "13.png": {
        "image_url": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&w=1200&q=80",
        "category": "Analytics", "category_slug": "analytics",
        "badge": "Network Telemetry",
        "tags": "Network Telemetry, Real-Time Graph, Web Plotter",
        "featured": False,
    },
    "14.png": {
        "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80",
        "category": "Analytics", "category_slug": "analytics",
        "badge": "Monitoring Daemon",
        "tags": "Remote Server, Cron Monitor, Health Check",
        "featured": False,
    },
    "15.png": {
        "image_url": "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=1200&q=80",
        "category": "Analytics", "category_slug": "analytics",
        "badge": "Data Visualization",
        "tags": "Matplotlib, Data Pipeline, Visual Analytics",
        "featured": False,
    },
    "16.png": {
        "image_url": "https://images.unsplash.com/photo-1534088568595-a066f410bcda?auto=format&fit=crop&w=1200&q=80",
        "category": "Analytics", "category_slug": "analytics",
        "badge": "Weather Dashboard",
        "tags": "5-Day Forecast, Data Charts, API Client",
        "featured": False,
    },
    "17.png": {
        "image_url": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1200&q=80",
        "category": "Desktop GUI", "category_slug": "desktop",
        "badge": "PyQt6 & SQL",
        "tags": "PyQt6 Desktop, SQLite DB, Admin Dashboard",
        "featured": False,
    },
    "18.png": {
        "image_url": "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=1200&q=80",
        "category": "Desktop GUI", "category_slug": "desktop",
        "badge": "PyQt6 & SQL",
        "tags": "PyQt6 Desktop, Relational SQL, Academic Ops",
        "featured": False,
    },
    "19.png": {
        "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
        "category": "Web Application", "category_slug": "web",
        "badge": "Django Web App",
        "tags": "Django, Real-Time Menu, Dynamic Filters",
        "featured": True,
    },
    "20.png": {
        "image_url": "https://images.unsplash.com/photo-1472851294608-062f824d29cc?auto=format&fit=crop&w=1200&q=80",
        "category": "Web Application", "category_slug": "web",
        "badge": "Django E-Commerce",
        "tags": "Django E-Commerce, Order Processing, Seller Portal",
        "featured": True,
    },
}

SERVICES_DATA = [
    {
        "title": "Custom Full Stack Web Applications",
        "category": "FULL STACK ARCHITECTURE",
        "description": "End-to-end bespoke web platforms architected with Django, Python, and modern responsive frontends. Built with domain-driven design, robust ORM modeling, role-based access control (RBAC), secure authentication flows, and high-performance server-side rendering.",
        "deliverables": "Modular Django / Flask Core Engine\nDynamic Responsive UI with Vanilla JS\nRole-Based Permissions & Auth Systems\nUnit & Integration Test Coverage",
        "tags": "Django, Python, HTML5 / CSS3, JavaScript, SQLite / MySQL",
        "image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1200&q=80",
        "badge": "FLAGSHIP OFFERING",
    },
    {
        "title": "High Throughput REST APIs and Microservices",
        "category": "BACKEND AND MICROSERVICES",
        "description": "Stateless, scalable RESTful API backends and webhook microservices built with Django REST Framework and Flask. Engineered for low-latency JSON delivery, granular token authentication (JWT / Bearer), rate-limiting, and comprehensive Swagger/OpenAPI interactive documentation.",
        "deliverables": "Stateless REST Microservice Endpoints\nJWT & Token-Based Authentication\nAutomated OpenAPI / Swagger Interactive Docs\nRate Limiting, Throttling & Caching",
        "tags": "Django REST Framework, Flask, JSON API, Redis Caching, Postman",
        "image_url": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1200&q=80",
        "badge": "MICROSERVICES",
    },
    {
        "title": "Relational Database Architecture and Query Tuning",
        "category": "DATABASE AND STORAGE",
        "description": "High-integrity relational schema design, 3NF normalization, index optimization, and transaction management. Specialized in tuning slow database queries, eliminating N+1 ORM bottlenecks, managing non-destructive migrations, and ensuring ACID consistency.",
        "deliverables": "Normalized Relational Schema Architecture\nIndex Optimization & Query Profiling\nACID Transactions & Row-Level Locking\nNon-Destructive Migration Scripts",
        "tags": "MySQL, PostgreSQL, SQLite, Django ORM, SQL Profiling",
        "image_url": "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?auto=format&fit=crop&w=1200&q=80",
        "badge": "DATA INTEGRITY",
    },
    {
        "title": "Automated Data Pipelines and Web Scraping",
        "category": "DATA EXTRACTION AND ETL",
        "description": "Automated data harvesting, cleansing, transformation, and ingestion pipelines. Built with BeautifulSoup, Selenium, and background scheduling to reliably extract unstructured web data, parse dynamic JavaScript pages, validate schemas, and sync cleanly into production databases.",
        "deliverables": "Headless Multi-Threaded Scraping Engines\nAnti-Bot Handling & Proxy Support\nSchema Validation & ETL Normalization\nAutomated Scheduled Execution",
        "tags": "Python, BeautifulSoup, Selenium, Pandas ETL, Cron Automation",
        "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
        "badge": "AUTOMATION",
    },
    {
        "title": "Computer Vision and Intelligent Image Systems",
        "category": "COMPUTER VISION AND AI",
        "description": "Real-time video stream processing, motion detection, contour analysis, and automated image transformation pipelines using OpenCV and NumPy. Developing computer vision tools that integrate seamlessly with web services and standalone automated workflows.",
        "deliverables": "Live Webcam Frame Analysis & Motion Tracking\nContour Detection & Visual Filtering\nAutomated Batch Image Processing\nMatplotlib & OpenCV Stream Integration",
        "tags": "OpenCV, Python, NumPy, Computer Vision, Matplotlib",
        "image_url": "https://images.unsplash.com/photo-1507146426996-ef05306b995a?auto=format&fit=crop&w=1200&q=80",
        "badge": "VISION AND AI",
    },
    {
        "title": "Cross Platform Desktop GUI and Enterprise Tools",
        "category": "DESKTOP APPLICATIONS",
        "description": "Native graphical user interface desktop applications built with PyQt6 / PySide. Tailored for administrative dashboards, offline database tools, school and student management portals, automated PDF invoice generation, and custom internal enterprise software.",
        "deliverables": "Native Cross-Platform GUI (Windows / macOS / Linux)\nEmbedded SQLite Local Database Support\nAutomated PDF & Excel Export Engines\nStandalone Executable Packaging",
        "tags": "PyQt6, Python, Qt Designer, ReportLab PDF, SQLite",
        "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80",
        "badge": "DESKTOP SUITE",
    },
]


class Command(BaseCommand):
    help = 'Import existing projects from data.csv and hardcoded services into the database.'

    def handle(self, *args, **options):
        self._import_projects()
        self._import_services()

    def _import_projects(self):
        csv_path = settings.BASE_DIR / 'data.csv'
        if not csv_path.exists():
            self.stderr.write(self.style.WARNING('data.csv not found — skipping project import.'))
            return

        created = 0
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for index, row in enumerate(reader, start=1):
                img_key = row.get('image', f'{index}.png').strip()
                meta = PROJECT_METADATA.get(img_key, {})

                raw_url = row.get('url', '').strip()
                if raw_url.endswith('.png'):
                    repo_url = 'https://github.com/nabilmushfique460'
                else:
                    repo_url = raw_url

                obj, was_created = Project.objects.get_or_create(
                    title=row.get('title', '').strip(),
                    defaults={
                        'description': row.get('description', '').strip(),
                        'url': repo_url,
                        'image_url': meta.get('image_url', ''),
                        'category': meta.get('category', 'Software'),
                        'category_slug': meta.get('category_slug', 'all'),
                        'badge': meta.get('badge', ''),
                        'tags': meta.get('tags', ''),
                        'featured': meta.get('featured', False),
                        'order': index,
                    },
                )
                if was_created:
                    created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Projects: {created} created, {Project.objects.count()} total.'
        ))

    def _import_services(self):
        created = 0
        for index, svc in enumerate(SERVICES_DATA, start=1):
            obj, was_created = Service.objects.get_or_create(
                title=svc['title'],
                defaults={
                    'category': svc.get('category', ''),
                    'description': svc.get('description', ''),
                    'deliverables': svc.get('deliverables', ''),
                    'tags': svc.get('tags', ''),
                    'image_url': svc.get('image_url', ''),
                    'badge': svc.get('badge', ''),
                    'order': index,
                },
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Services: {created} created, {Service.objects.count()} total.'
        ))

