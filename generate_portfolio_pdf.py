"""
Generate a Publication-Grade Comprehensive PDF Document for S.M. Nabil Mushfique's
Django & Python Portfolio Website with Full Technical Details.
"""
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

# Numbered Canvas for professional "Page X of Y" footer and running header
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Draw running header on pages > 1
        if self._pageNumber > 1:
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(40, letter[1] - 35, letter[0] - 40, letter[1] - 35)
            self.drawString(40, letter[1] - 30, "S.M. NABIL MUSHFIOUE  |  PORTFOLIO & CAPABILITIES DOSSIER")
            self.drawRightString(letter[0] - 40, letter[1] - 30, "DJANGO & PYTHON FULL-STACK")
        
        # Draw running footer on all pages
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(40, 40, letter[0] - 40, 40)
        self.drawString(40, 28, "CONFIDENTIAL & PROPRIETARY  •  Portfolio Website Dossier  •  github.com/nabilmushfique460")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 40, 28, page_text)
        self.restoreState()


def build_portfolio_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=45,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom color palette
    c_primary = colors.HexColor("#0F172A")    # Deep Navy Slate
    c_accent = colors.HexColor("#4F46E5")     # Indigo
    c_cyan = colors.HexColor("#0284C7")       # Bright Cyan
    c_dark = colors.HexColor("#1E293B")       # Slate Dark
    c_muted = colors.HexColor("#64748B")      # Muted Slate
    c_card_bg = colors.HexColor("#F8FAFC")    # Very light slate
    c_tag_bg = colors.HexColor("#EEF2F6")     # Tag pill bg
    c_border = colors.HexColor("#CBD5E1")     # Border
    c_gold = colors.HexColor("#D97706")       # Amber

    # Custom Paragraph Styles
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_primary,
        alignment=TA_LEFT
    )
    style_cover_sub = ParagraphStyle(
        'CoverSub',
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_accent,
        alignment=TA_LEFT
    )
    style_section_title = ParagraphStyle(
        'SectionTitle',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=6
    )
    style_subsection_title = ParagraphStyle(
        'SubSectionTitle',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=c_accent,
        spaceBefore=6,
        spaceAfter=3
    )
    style_body = ParagraphStyle(
        'CustomBody',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_dark,
        alignment=TA_LEFT
    )
    style_body_bold = ParagraphStyle(
        'CustomBodyBold',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=c_dark,
    )
    style_body_muted = ParagraphStyle(
        'CustomBodyMuted',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_muted,
    )
    style_badge = ParagraphStyle(
        'BadgeStyle',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.white,
        alignment=TA_CENTER
    )
    style_stat_num = ParagraphStyle(
        'StatNum',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=20,
        textColor=c_accent,
        alignment=TA_CENTER
    )
    style_stat_lbl = ParagraphStyle(
        'StatLbl',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=c_muted,
        alignment=TA_CENTER
    )

    story = []

    # ==========================================
    # PAGE 1: EXECUTIVE COVER & PROFILE OVERVIEW
    # ==========================================
    # Top decorative banner box
    banner_data = [
        [
            Paragraph("<b>S.M. NABIL MUSHFIOUE</b><br/><font size=10 color='#6366F1'>FULL-STACK PYTHON & DJANGO SOFTWARE ENGINEER</font>", style_cover_title),
            Paragraph("<b>PORTFOLIO DOSSIER</b><br/><font size=8 color='#64748B'>VERSION 2026.1 • PRODUCTION READY</font><br/><font size=8 color='#0284C7'>github.com/nabilmushfique460</font>", ParagraphStyle('RHead', parent=style_body, alignment=TA_RIGHT))
        ]
    ]
    banner_table = Table(banner_data, colWidths=[340, 192])
    banner_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(banner_table)
    story.append(HRFlowable(width="100%", thickness=2, color=c_accent, spaceBefore=4, spaceAfter=12))

    # Executive Summary Card
    summary_text = (
        "<b>Executive Profile:</b> High-impact Software Engineer specializing in scalable full-stack web architectures, "
        "robust Python backend engineering, Django ecosystem development, RESTful microservices, and database performance tuning. "
        "Proven track record delivering <b>20+ production-grade software projects</b> spanning enterprise web platforms, "
        "headless automated ETL pipelines, computer vision systems, and native cross-platform desktop administrative suites."
    )
    summary_table = Table([[Paragraph(summary_text, style_body)]], colWidths=[532])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_card_bg),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 10))

    # Metrics Highlights Bar (4 Columns)
    stats_data = [
        [
            Paragraph("20+", style_stat_num),
            Paragraph("100%", style_stat_num),
            Paragraph("6", style_stat_num),
            Paragraph("0ms", style_stat_num)
        ],
        [
            Paragraph("PRODUCTION APPS", style_stat_lbl),
            Paragraph("TESTED ARCHITECTURE", style_stat_lbl),
            Paragraph("CORE DOMAIN AREAS", style_stat_lbl),
            Paragraph("SECURITY COMPLIANCE", style_stat_lbl)
        ]
    ]
    stats_table = Table(stats_data, colWidths=[133, 133, 133, 133])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(stats_table)
    story.append(Spacer(1, 12))

    # Core Technical Arsenal Grid
    story.append(Paragraph("Core Technical Stack & Engineering Competencies", style_section_title))
    
    skills_data = [
        [
            Paragraph("<b>Backend & Web Frameworks</b><br/><font color='#64748B'>Django 6.x, Django REST Framework, Flask, Python 3.12+, ASGI/WSGI, Gunicorn, Celery, Whitenoise</font>", style_body),
            Paragraph("<b>Frontend & UI/UX</b><br/><font color='#64748B'>Vanilla JavaScript (ES6+), HTML5, CSS3 / Modern Flex & Grid, Responsive UI, Glassmorphism, Micro-interactions</font>", style_body)
        ],
        [
            Paragraph("<b>Databases & Caching</b><br/><font color='#64748B'>PostgreSQL, MySQL, SQLite3, Django ORM, 3NF Normalization, Index Optimization, Redis Caching</font>", style_body),
            Paragraph("<b>AI, Vision & Automation</b><br/><font color='#64748B'>OpenCV, NumPy, Matplotlib, BeautifulSoup4, Selenium, OpenPyXL, ReportLab PDF, NLP APIs</font>", style_body)
        ],
        [
            Paragraph("<b>Desktop & Native GUI</b><br/><font color='#64748B'>PyQt6, PySide, Qt Designer, Cross-Platform Desktop Packaging (Windows/macOS/Linux), Local DB Engines</font>", style_body),
            Paragraph("<b>DevOps & Best Practices</b><br/><font color='#64748B'>Docker, Docker Compose, Git / GitHub CI/CD, Linux Server Admin, SMTP Email Routing, PEP 8, Clean Architecture</font>", style_body)
        ]
    ]
    skills_table = Table(skills_data, colWidths=[261, 261])
    skills_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_card_bg),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(skills_table)
    story.append(Spacer(1, 10))

    # Contact & Quick Links Box
    contact_data = [
        [
            Paragraph("<b>Direct Contact:</b> nabil29089@gmail.com", style_body),
            Paragraph("<b>GitHub:</b> github.com/nabilmushfique460", style_body),
            Paragraph("<b>Portfolio URL:</b> 127.0.0.1:8000", style_body)
        ]
    ]
    contact_table = Table(contact_data, colWidths=[180, 180, 172])
    contact_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#BFDBFE")),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(contact_table)

    story.append(PageBreak())

    # ==========================================
    # PAGE 2: SERVICES & OFFERINGS DOSSIER
    # ==========================================
    story.append(Paragraph("Professional Services & Architectural Solutions", style_cover_title))
    story.append(Paragraph("High-performance technical services delivered with strict quality benchmarks and domain-driven design.", style_cover_sub))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=4, spaceAfter=10))

    services_list = [
        {
            "id": "01",
            "title": "Custom Full Stack Web Applications",
            "cat": "FULL STACK ARCHITECTURE",
            "desc": "End-to-end bespoke web platforms architected with Django, Python, and modern responsive frontends. Built with domain-driven design, robust ORM modeling, role-based access control (RBAC), secure authentication flows, and high-performance server-side rendering.",
            "deliverables": "• Modular Django / Flask Core Engine  • Dynamic Responsive UI with Vanilla JS  • Role-Based Permissions & Auth Systems  • Unit & Integration Test Coverage",
            "tags": "Django • Python • HTML5 / CSS3 • JavaScript • SQLite / PostgreSQL"
        },
        {
            "id": "02",
            "title": "High Throughput REST APIs & Microservices",
            "cat": "BACKEND & MICROSERVICES",
            "desc": "Stateless, scalable RESTful API backends and webhook microservices built with Django REST Framework and Flask. Engineered for low-latency JSON delivery, granular token authentication (JWT / Bearer), rate-limiting, and comprehensive Swagger/OpenAPI documentation.",
            "deliverables": "• Stateless REST Microservice Endpoints  • JWT & Token-Based Authentication  • Automated OpenAPI / Swagger Interactive Docs  • Rate Limiting, Throttling & Caching",
            "tags": "Django REST Framework • Flask • JSON API • Redis Caching • Postman"
        },
        {
            "id": "03",
            "title": "Relational Database Architecture & Query Tuning",
            "cat": "DATABASE & STORAGE",
            "desc": "High-integrity relational schema design, 3NF normalization, index optimization, and transaction management. Specialized in tuning slow database queries, eliminating N+1 ORM bottlenecks, managing non-destructive migrations, and ensuring ACID consistency.",
            "deliverables": "• Normalized Relational Schema Architecture  • Index Optimization & Query Profiling  • ACID Transactions & Row-Level Locking  • Non-Destructive Migration Scripts",
            "tags": "PostgreSQL • MySQL • SQLite • Django ORM • SQL Profiling"
        },
        {
            "id": "04",
            "title": "Automated Data Pipelines & Web Scraping",
            "cat": "DATA EXTRACTION & ETL",
            "desc": "Automated data harvesting, cleansing, transformation, and ingestion pipelines. Built with BeautifulSoup, Selenium, and background scheduling to reliably extract unstructured web data, parse dynamic JavaScript pages, validate schemas, and sync cleanly into production databases.",
            "deliverables": "• Headless Multi-Threaded Scraping Engines  • Anti-Bot Handling & Proxy Support  • Schema Validation & ETL Normalization  • Automated Scheduled Execution",
            "tags": "Python • BeautifulSoup • Selenium • Pandas ETL • Cron Automation"
        },
        {
            "id": "05",
            "title": "Computer Vision & Intelligent Image Systems",
            "cat": "COMPUTER VISION & AI",
            "desc": "Real-time video stream processing, motion detection, contour analysis, and automated image transformation pipelines using OpenCV and NumPy. Developing computer vision tools that integrate seamlessly with web services and standalone automated workflows.",
            "deliverables": "• Live Webcam Frame Analysis & Motion Tracking  • Contour Detection & Visual Filtering  • Automated Batch Image Processing  • Matplotlib & OpenCV Stream Integration",
            "tags": "OpenCV • Python • NumPy • Computer Vision • Matplotlib"
        },
        {
            "id": "06",
            "title": "Cross-Platform Desktop GUI & Enterprise Tools",
            "cat": "DESKTOP APPLICATIONS",
            "desc": "Native graphical user interface desktop applications built with PyQt6 / PySide. Tailored for administrative dashboards, offline database tools, school and student management portals, automated PDF invoice generation, and custom internal enterprise software.",
            "deliverables": "• Native Cross-Platform GUI (Win/Mac/Linux)  • Embedded SQLite Local Database  • Automated PDF & Excel Export Engines  • Standalone Executable Packaging",
            "tags": "PyQt6 • Python • Qt Designer • ReportLab PDF • SQLite"
        }
    ]

    for svc in services_list:
        svc_content = [
            Paragraph(f"<font color='#4F46E5'><b>[{svc['id']}] {svc['cat']}</b></font> — <b><font size=10.5 color='#0F172A'>{svc['title']}</font></b>", style_body),
            Spacer(1, 2),
            Paragraph(f"<font color='#334155'>{svc['desc']}</font>", style_body),
            Spacer(1, 2),
            Paragraph(f"<font color='#0284C7'><b>Deliverables:</b></font> <font color='#475569'>{svc['deliverables']}</font>", style_body_muted),
            Paragraph(f"<font color='#64748B'><b>Technologies:</b> {svc['tags']}</font>", style_body_muted)
        ]
        svc_table = Table([[svc_content]], colWidths=[532])
        svc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), c_card_bg),
            ('BOX', (0, 0), (-1, -1), 0.75, c_border),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(svc_table)
        story.append(Spacer(1, 5))

    story.append(PageBreak())

    # ==========================================
    # PAGE 3: COMPLETE PROJECT PORTFOLIO (1-10)
    # ==========================================
    story.append(Paragraph("Projects Catalog — Web Applications, APIs & Automation", style_cover_title))
    story.append(Paragraph("Comprehensive catalog of implemented, production-tested software systems (Projects 01 to 10 of 20).", style_cover_sub))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=4, spaceAfter=8))

    projects_p1 = [
        {
            "id": "01",
            "title": "Django Task Flow & Management Platform",
            "cat": "Web Application",
            "badge": "Django & Python",
            "tags": "Django • Python • Full-Stack • Task Flow",
            "desc": "Architected a full-lifecycle Django web application featuring robust task creation, multi-attribute status pipelines, dynamic filtering, deadline notifications, and responsive UI components with persistent SQLite database storage.",
            "url": "github.com/nabilmushfique460"
        },
        {
            "id": "02",
            "title": "Responsive Python Portfolio & Showcase Engine",
            "cat": "Web Application",
            "badge": "Full-Stack Python",
            "tags": "Python • Vanilla JS • Responsive UI",
            "desc": "Engineered a high-performance personal portfolio platform utilizing dynamic CSV ingestion, customized Django template inheritance, responsive CSS grid layouts, and active SMTP email communication pipelines.",
            "url": "github.com/nabilmushfique460"
        },
        {
            "id": "03",
            "title": "Automated PDF Document & Invoice Generator",
            "cat": "Automation",
            "badge": "PDF Automation",
            "tags": "Python • PDF Generator • Document Engine",
            "desc": "Built an automated document compilation engine leveraging ReportLab and FPDF to programmatically assemble structured business invoices, analytical reports, and data certificates from dynamic input datasets.",
            "url": "github.com/nabilmushfique460"
        },
        {
            "id": "04",
            "title": "Excel Data Pipeline & Spreadsheet Compiler",
            "cat": "Automation",
            "badge": "Excel & PDF Engine",
            "tags": "OpenPyXL • PDF Toolkit • ETL Process",
            "desc": "Constructed an automated spreadsheet processing script using OpenPyXL to ingest multi-sheet tabular workbooks, calculate aggregate metrics, perform structural data validations, and render PDF summaries.",
            "url": "github.com/nabilmushfique460"
        },
        {
            "id": "05",
            "title": "Real-Time News Sentiment & NLP Analyzer",
            "cat": "AI & Data",
            "badge": "Sentiment NLP",
            "tags": "NLP Engine • News API • Sentiment AI",
            "desc": "Engineered an AI-assisted market intelligence script that queries live global news APIs, processes article text using natural language sentiment classification algorithms, and visualizes market tone distributions.",
            "url": "github.com/nabilmushfique460"
        },
        {
            "id": "06",
            "title": "Flask Weather Telemetry & Forecast Microservice",
            "cat": "REST API",
            "badge": "Flask Microservice",
            "tags": "Flask • RESTful API • JSON Feed",
            "desc": "Deployed a lightweight Flask microservice providing structured RESTful endpoints for meteorological forecasting, integrating with remote weather APIs, and formatting serialized JSON response payloads.",
            "url": "github.com/nabilmushfique460"
        },
        {
            "id": "07",
            "title": "Hotel & Hospitality Reservation Engine",
            "cat": "Web Application",
            "badge": "Booking Engine",
            "tags": "Python • Booking Architecture • UX Flow",
            "desc": "Developed a comprehensive room reservation and hospitality booking interface with date-range room availability verification, customer confirmation emails, and administrative occupancy monitoring.",
            "url": "github.com/nabilmushfique460"
        },
        {
            "id": "08",
            "title": "Headless Event Scraper & Instant Email Alerter",
            "cat": "Automation",
            "badge": "Web Scraping",
            "tags": "BeautifulSoup • SMTP Mailer • Event Monitor",
            "desc": "Authored an automated web scraping daemon using BeautifulSoup that monitors target concert and conference websites, detects newly published tour dates, and triggers instant automated SMTP email notifications.",
            "url": "github.com/nabilmushfique460"
        },
        {
            "id": "09",
            "title": "Domain Assistant & Conversational Knowledge Agent",
            "cat": "AI & Data",
            "badge": "Domain Assistant",
            "tags": "Knowledge Base • AI Agent • NLP Queries",
            "desc": "Built an interactive question-answering assistant that indexes domain knowledge documents, accepts natural language queries from terminal or web, and provides contextualized synthesized responses.",
            "url": "github.com/nabilmushfique460"
        },
        {
            "id": "10",
            "title": "Social Messaging Bot & Conversational Gateway",
            "cat": "AI & Data",
            "badge": "Conversational AI",
            "tags": "Facebook API • NLP Engine • Chat Gateway",
            "desc": "Integrated a webhook-driven conversational bot with the Facebook Graph API to automate customer inquiry handling, recognize intent patterns, and provide automated multi-turn customer support.",
            "url": "github.com/nabilmushfique460"
        }
    ]

    for p in projects_p1:
        p_data = [
            [
                Paragraph(f"<b>#{p['id']} {p['title']}</b>", style_body_bold),
                Paragraph(f"<font color='#4F46E5'><b>{p['badge']}</b></font> | <font color='#0284C7'>{p['cat']}</font>", ParagraphStyle('RTag', parent=style_body, alignment=TA_RIGHT))
            ],
            [
                Paragraph(f"<font color='#334155'>{p['desc']}</font><br/><font color='#64748B'><b>Stack:</b> {p['tags']}  •  <b>Repo:</b> {p['url']}</font>", style_body),
                ""
            ]
        ]
        p_table = Table(p_data, colWidths=[360, 172])
        p_table.setStyle(TableStyle([
            ('SPAN', (0, 1), (1, 1)),
            ('BACKGROUND', (0, 0), (-1, -1), c_card_bg),
            ('BOX', (0, 0), (-1, -1), 0.5, c_border),
            ('PADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 1), (-1, 1), 5),
        ]))
        story.append(p_table)
        story.append(Spacer(1, 3.5))

    story.append(PageBreak())

    # ==========================================
    # PAGE 4: COMPLETE PROJECT PORTFOLIO (11-20)
    # ==========================================
    story.append(Paragraph("Projects Catalog — Vision, Analytics, Desktop & E-Commerce", style_cover_title))
    story.append(Paragraph("Comprehensive catalog of implemented, production-tested software systems (Projects 11 to 20 of 20).", style_cover_sub))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=4, spaceAfter=8))

    projects_p2 = [
        {
            "id": "11",
            "title": "Computer Vision Security & Motion Detection System",
            "cat": "AI & Data",
            "badge": "Computer Vision",
            "tags": "OpenCV • Motion Detection • Email Trigger",
            "desc": "Architected a real-time computer vision security script utilizing OpenCV to analyze live camera frames, calculate background differential contours, detect unauthorized motion, and transmit captured photo frames via automated email.",
            "url": "github.com/nabilmushfique460"
        },
        {
            "id": "12",
            "title": "System Keystroke Telemetry & Productivity Analytics",
            "cat": "Analytics",
            "badge": "Keystroke Analytics",
            "tags": "Keyboard Hook • Word Analytics • Stats Daemon",
            "desc": "Built a background operating system telemetry daemon that records typing frequency, performs word count aggregations, and produces analytical productivity metrics without degrading user latency.",
            "url": "github.com/nabilmushfique460"
        },
        {
            "id": "13",
            "title": "Network Traffic Telemetry & Real-Time Grapher",
            "cat": "Analytics",
            "badge": "Network Telemetry",
            "tags": "Network Telemetry • Real-Time Graph • Web Plotter",
            "desc": "Implemented a network telemetry tool monitoring real-time packet ingress/egress, logging historical bandwidth utilization metrics, and rendering interactive web charts using Matplotlib and Bokeh.",
            "url": "github.com/nabilmushfique460"
        },
        {
            "id": "14",
            "title": "Distributed Server Health Monitoring Daemon",
            "cat": "Analytics",
            "badge": "Monitoring Daemon",
            "tags": "Remote Server • Cron Monitor • Health Check",
            "desc": "Constructed an automated server health monitor running scheduled background cron jobs to ping remote HTTP endpoints, verify database availability, and dispatch alert messages upon service degradation.",
            "url": "github.com/nabilmushfique460"
        },
        {
            "id": "15",
            "title": "Data Science Analytics Pipeline & Visual Dashboard",
            "cat": "Analytics",
            "badge": "Data Visualization",
            "tags": "Matplotlib • Data Pipeline • Visual Analytics",
            "desc": "Built a comprehensive Python data visualization toolkit ingesting multi-variable CSV datasets, conducting statistical aggregation, and rendering publishable scientific scatter plots and bar distributions.",
            "url": "github.com/nabilmushfique460"
        },
        {
            "id": "16",
            "title": "5-Day Weather Forecast & Historical Analytics Tool",
            "cat": "Analytics",
            "badge": "Weather Dashboard",
            "tags": "5-Day Forecast • Data Charts • API Client",
            "desc": "Authored an analytical desktop dashboard querying OpenWeatherMap REST endpoints, processing multi-day barometric pressure and temperature time-series arrays, and rendering comparative trend lines.",
            "url": "github.com/nabilmushfique460"
        },
        {
            "id": "17",
            "title": "Enterprise Academic & Student Management Desktop GUI",
            "cat": "Desktop GUI",
            "badge": "PyQt6 & SQL",
            "tags": "PyQt6 Desktop • SQLite DB • Admin Dashboard",
            "desc": "Designed a native desktop application in PyQt6 providing student registration, enrollment records management, dynamic search filters, relational SQLite persistence, and instant grade transcript generation.",
            "url": "github.com/nabilmushfique460"
        },
        {
            "id": "18",
            "title": "Institutional Operations & Course Administrative Suite",
            "cat": "Desktop GUI",
            "badge": "PyQt6 & SQL",
            "tags": "PyQt6 Desktop • Relational SQL • Academic Ops",
            "desc": "Created a standalone administrative desktop suite built with PySide/PyQt6 enabling staff to organize academic departments, manage faculty assignments, and export comprehensive audit records.",
            "url": "github.com/nabilmushfique460"
        },
        {
            "id": "19",
            "title": "Django Dynamic Restaurant Ordering & Menu Engine",
            "cat": "Web Application",
            "badge": "Django Web App",
            "tags": "Django • Real-Time Menu • Dynamic Filters",
            "desc": "Engineered a responsive Django food ordering platform with real-time category filtering, ingredient customization, dynamic shopping cart session state, and order summary generation.",
            "url": "github.com/nabilmushfique460"
        },
        {
            "id": "20",
            "title": "Django Multi-Vendor E-Commerce Platform",
            "cat": "Web Application",
            "badge": "Django E-Commerce",
            "tags": "Django E-Commerce • Order Processing • Seller Portal",
            "desc": "Developed a full-featured e-commerce platform incorporating product catalog management, seller dashboards, customer shopping cart workflows, secure checkout processing, and automated transactional receipts.",
            "url": "github.com/nabilmushfique460"
        }
    ]

    for p in projects_p2:
        p_data = [
            [
                Paragraph(f"<b>#{p['id']} {p['title']}</b>", style_body_bold),
                Paragraph(f"<font color='#4F46E5'><b>{p['badge']}</b></font> | <font color='#0284C7'>{p['cat']}</font>", ParagraphStyle('RTag2', parent=style_body, alignment=TA_RIGHT))
            ],
            [
                Paragraph(f"<font color='#334155'>{p['desc']}</font><br/><font color='#64748B'><b>Stack:</b> {p['tags']}  •  <b>Repo:</b> {p['url']}</font>", style_body),
                ""
            ]
        ]
        p_table = Table(p_data, colWidths=[360, 172])
        p_table.setStyle(TableStyle([
            ('SPAN', (0, 1), (1, 1)),
            ('BACKGROUND', (0, 0), (-1, -1), c_card_bg),
            ('BOX', (0, 0), (-1, -1), 0.5, c_border),
            ('PADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 1), (-1, 1), 5),
        ]))
        story.append(p_table)
        story.append(Spacer(1, 3.5))

    story.append(PageBreak())

    # ==========================================
    # PAGE 5: ARCHITECTURE, DEPLOYMENT & CONTACT
    # ==========================================
    story.append(Paragraph("Architectural Standards & Engagement Protocol", style_cover_title))
    story.append(Paragraph("Enterprise-grade engineering methodologies, deployment pipelines, and collaboration workflows.", style_cover_sub))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=4, spaceAfter=10))

    arch_data = [
        [
            Paragraph("<b>1. Clean Code & Modular Architecture</b><br/><font color='#475569'>Every Django app is strictly partitioned into domain-specific modules with explicit service layers, custom managers, decoupled forms, and encapsulated business logic avoiding fat views or bloated models.</font>", style_body),
            Paragraph("<b>2. Rigorous Security Standards</b><br/><font color='#475569'>Protection against CSRF, SQL Injection, and XSS. Implemented strict environment variable segregation (.env), secure cookie policies, role-based access control (RBAC), and sanitization filters.</font>", style_body)
        ],
        [
            Paragraph("<b>3. Scalable Database Engineering</b><br/><font color='#475569'>Normalized relational schemas (PostgreSQL / MySQL / SQLite), optimized index planning, transaction atomicity, query count profiling, and elimination of N+1 ORM bottlenecks via select_related / prefetch_related.</font>", style_body),
            Paragraph("<b>4. Automated Testing & Continuous Integration</b><br/><font color='#475569'>Comprehensive unit and integration test coverage using Django TestCase and PyTest. Verified schema migrations, deterministic data fixtures, and automated GitHub Actions CI/CD workflows.</font>", style_body)
        ]
    ]
    arch_table = Table(arch_data, colWidths=[261, 261])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_card_bg),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 14))

    # Project Engagement & Delivery Timeline
    story.append(Paragraph("Client Engagement & Project Delivery Phases", style_section_title))
    
    phases_data = [
        [
            Paragraph("<b>Phase 1: Discovery & Architecture</b><br/><font color='#64748B'>Requirement mapping, schema design, API contract definition, and milestone scoping.</font>", style_body),
            Paragraph("<b>Phase 2: Sprint Development</b><br/><font color='#64748B'>Agile milestone iterations, core backend logic, frontend UI synthesis, and database modeling.</font>", style_body),
            Paragraph("<b>Phase 3: QA, Hardening & Delivery</b><br/><font color='#64748B'>Stress testing, security review, Dockerization, documentation, and production deployment.</font>", style_body)
        ]
    ]
    phases_table = Table(phases_data, colWidths=[174, 174, 174])
    phases_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(phases_table)
    story.append(Spacer(1, 16))

    # Formal Contact & Call To Action Banner
    cta_data = [
        [
            Paragraph("<b>Ready to Build or Scale Your Software Platform?</b><br/><font size=9.5 color='#334155'>Available for full-stack web application development, custom API microservices, database performance consulting, and bespoke Python software automation.</font><br/><br/>"
                      "<b>Primary Email:</b> <font color='#4F46E5'>nabil29089@gmail.com</font> &nbsp;&nbsp;•&nbsp;&nbsp; "
                      "<b>GitHub Portfolio:</b> <font color='#0284C7'>github.com/nabilmushfique460</font><br/>"
                      "<b>Website:</b> <font color='#0F172A'>Django Portfolio Live Instance (Local / Production)</font>", style_body)
        ]
    ]
    cta_table = Table(cta_data, colWidths=[532])
    cta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor("#6366F1")),
        ('PADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(cta_table)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] High-quality portfolio PDF generated at: {output_path}")


if __name__ == '__main__':
    project_dir = os.path.dirname(os.path.abspath(__file__))
    artifacts_dir = r"C:\Users\NABIL\.gemini\antigravity-ide\brain\97472252-df7c-4787-8965-8a337eb0344f"
    
    output_local = os.path.join(project_dir, "S.M._Nabil_Mushfique_Portfolio_Dossier.pdf")
    output_artifact = os.path.join(artifacts_dir, "S.M._Nabil_Mushfique_Portfolio_Dossier.pdf")
    
    build_portfolio_pdf(output_local)
    build_portfolio_pdf(output_artifact)
