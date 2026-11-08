# Full-Stack Developer Portfolio (Django)

A high-performance, dark-themed engineering portfolio built with **Python & Django**, designed with a modern typography-driven aesthetic, live project search and filtering, simulated live terminal deployment animation, and database-backed inquiries with automated SMTP email notifications.

---

## 🚀 Key Features

* **Live Interactive Terminal:** Custom JavaScript typewriter terminal on the hero landing page showing real-time health and deployment status.
* **Filterable & Searchable Projects Showcase:** 20 production-tested projects loaded from database models, featuring instant full-text search, category pills (`Web Apps`, `REST APIs`, `Automation`, `AI & Data`, `Analytics`, `Desktop GUI`), and tags.
* **Technical Offerings Breakdown:** 6 core engineering domains with itemized deliverables, technology chips, and curated visuals.
* **Persistent Contact & Notification Pipeline:**
  * Submissions stored reliably in SQLite (`ContactMessage` model) with Django Admin integration.
  * Anti-bot spam protection via hidden honeypot validation.
  * Post/Redirect/Get (PRG) pattern preventing duplicate submissions on page refresh.
  * Automated confirmation receipt to the inquiry sender and notification to the site administrator.
  * Graceful handling and status alerts if SMTP delivery is delayed.
* **Production-Grade Static Asset Delivery:** WhiteNoise integration with compression, caching, and automatic `STATIC_ROOT` handling.
* **Security & Environment Decoupling:** Credentials, secret keys, debug flags, and SMTP configuration isolated in `.env` via `python-dotenv`.
* **Containerized & CI-Ready:** Dockerfile with multi-worker Gunicorn server, Docker Compose with persistent data volumes, and automated GitHub Actions CI test suite.

---

## 🛠️ Tech Stack

* **Backend:** Python 3.11+, Django 5.2
* **Production Server:** Gunicorn, WhiteNoise
* **Database:** SQLite3 (ORM-backed with migrations)
* **Frontend:** Django Templates, Vanilla JavaScript, Modern CSS3 (CSS Grid, Flexbox, Keyframe Animations)
* **Email System:** Django SMTP Backend (Gmail TLS / Port 587)
* **CI/CD & Containers:** Docker, Docker Compose, GitHub Actions
* **Configuration:** `python-dotenv`

---

## 📦 Getting Started

### 1. Prerequisites
Ensure you have Python 3.11+ installed.

### 2. Set Up a Virtual Environment

```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and configure your credentials:

```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and fill in your settings:
```env
SECRET_KEY=your-secure-random-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,testserver

# Gmail SMTP Configuration
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-google-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

### 5. Run Database Migrations & Data Seeding

```bash
python manage.py migrate
python manage.py seed_data
```

### 6. Run the Test Suite

```bash
python manage.py test
```

### 7. Launch the Development Server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## 🐳 Docker Deployment

To run the application inside Docker with production-ready Gunicorn and persistent volumes:

```bash
docker compose up --build -d
```

The container exposes port `8000` and automatically mounts `./db.sqlite3` and `./media` for persistent data retention.

---

## 📂 Project Structure

```
Demo-Portfolio/
├── manage.py                  # Django administrative CLI
├── data.csv                   # Seed data source for projects
├── db.sqlite3                 # Local SQLite database (git-ignored)
├── requirements.txt           # Project dependencies
├── Dockerfile                 # Container image specification (Gunicorn)
├── docker-compose.yml         # Container orchestrator with persistent volumes
├── .env                       # Local environment variables (git-ignored)
├── .env.example               # Environment variables template
├── .gitignore                 # Comprehensive git ignore rules
├── .github/workflows/ci.yml   # Automated GitHub Actions test pipeline
├── mysite/                    # Project package configuration
│   ├── settings.py            # Environment-driven settings, WhiteNoise & security
│   ├── urls.py                # Root routing & admin delegation
│   ├── wsgi.py                # WSGI entrypoint
│   └── asgi.py                # ASGI entrypoint
└── portfolio/                 # Core portfolio application
    ├── admin.py               # Django admin interface for Project, Service, ContactMessage
    ├── apps.py                # Portfolio application configuration
    ├── forms.py               # ContactForm with anti-bot honeypot
    ├── models.py              # Models & properties (display_id, display_image, tags_list)
    ├── tests.py               # Automated unit, integration, and security tests
    ├── urls.py                # Application routes (/, about/, services/, contact/)
    ├── views.py               # View controllers with ORM aggregation & PRG handling
    ├── static/                # Static assets
    │   ├── css/style.css      # Dark-mode styling, glows, animations
    │   └── images/            # Static imagery & profile assets
    └── templates/             # HTML templates
        ├── base.html          # Shell layout, navbar & mobile drawer
        ├── home.html          # Hero section & live terminal animation
        ├── about.html         # Project showcase, search & filter pills
        ├── services.html      # Engineering offerings & deliverables
        └── contact.html       # Contact dossier, PRG alerts & inquiries
```

---

## 🧪 Testing

The project includes unit and integration tests covering GET and POST workflows, database persistence, email dispatch, anti-bot honeypots, and model helper properties.

Run the test suite with:
```bash
python manage.py test
```
