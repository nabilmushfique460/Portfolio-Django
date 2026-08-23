#!/bin/bash
# ====================================================================
# PythonAnywhere Server Update & Deployment Script
# Domain: https://nabil371.pythonanywhere.com/
# ====================================================================

set -e

echo "➡️ Navigating to project directory..."
cd /home/nabil371/Portfolio-Django || cd "$(dirname "$0")"

echo "➡️ Pulling latest changes from GitHub..."
git pull origin master || git pull

echo "➡️ Activating virtual environment..."
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "➡️ Installing/Updating Python dependencies..."
pip install -r requirements.txt

echo "➡️ Applying database migrations..."
python manage.py migrate

echo "➡️ Collecting static files (CSS, JS, images)..."
python manage.py collectstatic --noinput

echo "➡️ Reloading PythonAnywhere web app..."
if [ -f "/var/www/nabil371_pythonanywhere_com_wsgi.py" ]; then
    touch /var/www/nabil371_pythonanywhere_com_wsgi.py
    echo "✅ Web app reloaded via WSGI touch!"
fi

echo "===================================================================="
echo "🎉 Update complete! Site is live at: https://nabil371.pythonanywhere.com/"
echo "===================================================================="
