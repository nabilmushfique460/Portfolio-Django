# PythonAnywhere Server Update Rule

Whenever the user asks to update the server or deploy changes, always provide the single-line command formatted specifically for this project:

```bash
cd /home/Nabil371/Portfolio-Django && git pull origin master && source .venv/bin/activate && pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput && touch /var/www/Nabil371_pythonanywhere_com_wsgi.py
```
