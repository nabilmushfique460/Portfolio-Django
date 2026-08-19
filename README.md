# Web Developer Portfolio (Django)

A simple, professional four-page Django site: Home, About, Services, Contact.

## How to run it

```bash
pip install django
cd portfolio_site
python manage.py migrate
python manage.py runserver
```

Then open http://127.0.0.1:8000/ in your browser.

## Project structure

```
portfolio_site/
├── manage.py
├── mysite/                 # project package (settings, urls)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── portfolio/               # the app
    ├── views.py             # home, about, services, contact views
    ├── urls.py               # /, about/, services/, contact/
    ├── forms.py               # ContactForm (name, email, message)
    ├── admin.py
    ├── templates/
    │   ├── base.html          # header, nav, footer + {% block content %}
    │   ├── home.html
    │   ├── about.html
    │   ├── services.html
    │   └── contact.html
    └── static/css/style.css   # soft blue + cream theme
```

## Notes / assumptions

- No database or models are used yet, per the setup requirements — all
  four pages are rendered from templates only, and the Services page
  lists services as static content rather than pulling from a
  `Service` model. If you'd like the database-driven version instead
  (a `Service` model + admin-manageable service list with images),
  that's a straightforward next step and I'm happy to build it.
- The Contact form validates and shows a "Thank you" message on
  success. It intentionally does **not** send email or save to a
  database, per the original spec.
- The service cards on the Services page don't include images, since
  no real image files were provided. Adding an `image` field to each
  card (or a `Service` model with an `ImageField`) is easy to add
  later.
