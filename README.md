# Full-Stack Developer Portfolio (Django)

A high-performance, dark-themed engineering portfolio built with **Python & Django**, designed with a modern typography-driven aesthetic, live project search and filtering, simulated live terminal deployment animation, and database-backed inquiries with automated SMTP email notifications.

---

## 🚀 Key Features

* **Live Interactive Terminal:** Custom JavaScript typewriter terminal on the hero landing page showing real-time health and deployment status.
* **Filterable & Searchable Projects Showcase:** 20 production-tested projects loaded from structured data, featuring instant full-text search, category pills (`Web Apps`, `REST APIs`, `Automation`, `AI & Data`, `Analytics`, `Desktop GUI`), and tags.
* **Technical Offerings Breakdown:** 6 core engineering domains with itemized deliverables, technology chips, and curated visuals.
* **Persistent Contact & Notification Pipeline:**
  * Submissions stored reliably in SQLite (`ContactMessage` model) with Django Admin integration.
  * Automated confirmation email dispatched to the inquiry sender.
  * Automated notification email dispatched to the portfolio owner.
* **Security & Environment Decoupling:** Credentials, secret keys, debug flags, and SMTP configuration isolated in `.env` via `python-dotenv`.
* **Zero-Warning Django 5.2 Architecture:** Configured with `BigAutoField`, fully tested test suite, and clean URL routing.

---

## 🛠️ Tech Stack

* **Backend:** Python 3.11+, Django 5.2
* **Database:** SQLite3 (ORM-backed with migrations)
* **Frontend:** Django Templates, Vanilla JavaScript, Modern CSS3 (CSS Grid, Flexbox, Keyframe Animations)
* **Email System:** Django SMTP Backend (Gmail TLS / Port 587)
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

### 5. Run Database Migrations

```bash
python manage.py migrate
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

## 📂 Project Structure

```
Demo-Portfolio/
├── manage.py                  # Django administrative CLI
├── data.csv                   # Project repository data
├── db.sqlite3                 # SQLite relational database
├── requirements.txt           # Project dependencies
├── .env                       # Local environment variables (git-ignored)
├── .env.example               # Environment variables template
├── .gitignore                 # Comprehensive git ignore rules
├── mysite/                    # Project package configuration
│   ├── settings.py            # Environment-driven settings & security
│   ├── urls.py                # Root routing & admin delegation
│   ├── wsgi.py                # WSGI entrypoint
│   └── asgi.py                # ASGI entrypoint
└── portfolio/                 # Core portfolio application
    ├── admin.py               # ContactMessage Django admin interface
    ├── apps.py                # Portfolio application configuration
    ├── forms.py               # ContactForm ModelForm
    ├── models.py              # ContactMessage database model
    ├── tests.py               # Automated unit & integration tests
    ├── urls.py                # Application routes (/, about/, services/, contact/)
    ├── views.py               # View controllers & cached CSV data loader
    ├── static/                # Static assets
    │   ├── css/style.css      # Dark-mode styling, glows, animations
    │   └── images/            # Static imagery & profile assets
    └── templates/             # HTML templates
        ├── base.html          # Shell layout, navbar & mobile drawer
        ├── home.html          # Hero section & live terminal animation
        ├── about.html         # Project showcase, search & filter pills
        ├── services.html      # Engineering offerings & deliverables
        └── contact.html       # Direct channels & contact dossier
```

---

## 🧪 Testing

The project includes unit and integration tests covering GET and POST workflows, database persistence, email dispatch, and catalog integrity.

Run the test suite with:
```bash
python manage.py test
```
