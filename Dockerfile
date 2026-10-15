# ==============================================================================
# Dockerfile: Django Backend Container Build Specification
# ==============================================================================
# Builds the Python 3.11-slim container image for running the Django application.
#
# Key Steps:
# 1. Base Image: Official lightweight Python 3.11-slim.
# 2. OS Dependencies: Installs PostgreSQL client libraries (libpq-dev), GCC, and curl.
# 3. Python Packages: Installs dependencies from requirements.txt without caching.
# 4. Source Code: Mounts application code to /app.
# 5. Entrypoint: Launches Django development server on 0.0.0.0:8000.
# ==============================================================================

FROM python:3.11-slim

# Hata mesajlarını anlık görme + gereksiz .pyc dosyası oluşturma
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Sistem bağımlılıkları ve CA sertifikaları
RUN apt-get update && apt-get install -y \
    libpq-dev gcc ca-certificates fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

