# ==============================================================================
# Dockerfile: Django Backend İmaj Tanımı
# ==============================================================================
# Bu dosya, backend servisinin çalışacağı Docker container imajını adım adım inşa eder.
#
# Yapılan İşlemler:
# 1. Temel Sistem: Resmi hafif Python 3.11-slim imajını kullanır.
# 2. Sistem Bağımlılıkları: PostgreSQL (libpq-dev), GCC ve curl araçlarını yükler.
# 3. Python Bağımlılıkları: requirements.txt dosyasındaki tüm paketleri kurar.
# 4. Kod Kopyalama: Proje dosyalarını /app çalışma dizinine kopyalar.
# 5. Başlatma Komutu: Django yerleşik geliştirme sunucusunu 0.0.0.0:8000 üzerinde dinler.
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
