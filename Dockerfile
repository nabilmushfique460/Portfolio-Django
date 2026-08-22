# Use an official lightweight Python image
FROM python:3.12-slim

# Set environment variables:
# - PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files to disc
# - PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into the container
COPY . /app/

# Collect static files inside the image
RUN python manage.py collectstatic --noinput

# Expose port 8000 for Django web server
EXPOSE 8000

# Run migrations and start Django server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

