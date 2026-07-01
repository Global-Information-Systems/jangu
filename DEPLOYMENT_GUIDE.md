# 🚀 Production Deployment Guide

## Quick Start

### Prerequisites
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+
- Python 3.11+
- Nginx

### 1. Local Development Setup

```bash
# Clone repository
git clone https://github.com/tijuks/jangu.git
cd jangu

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver
```

### 2. Docker Deployment

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

### 3. Production Deployment

#### Configuration Checklist

```bash
# 1. Set environment variables
echo "SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')\" > .env
echo "DEBUG=False\" >> .env
echo "ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com\" >> .env

# 2. Setup SSL with Let's Encrypt
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --standalone -d yourdomain.com

# 3. Start services
docker-compose -f docker-compose.yml up -d

# 4. Setup SSL auto-renewal
sudo certbot renew --dry-run
```

### 4. Health Checks

```bash
# Check application
curl http://localhost:8000/health/

# Check database
docker-compose exec db pg_isready -U postgres

# Check Redis
docker-compose exec redis redis-cli ping
```

### 5. Database Backup

```bash
# Backup PostgreSQL
docker-compose exec db pg_dump -U postgres jangu > backup_$(date +%Y%m%d_%H%M%S).sql

# Automated daily backups
0 2 * * * cd /path/to/jangu && docker-compose exec db pg_dump -U postgres jangu > backups/backup_$(date +\%Y\%m\%d).sql
```

## Troubleshooting

#### Container won't start
```bash
docker-compose logs web
docker-compose down
docker-compose build --no-cache
docker-compose up
```

#### Database connection error
```bash
docker-compose ps db
docker-compose logs db
```
