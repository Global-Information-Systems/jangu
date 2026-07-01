# 🔒 Security Hardening Guide

## Authentication & Authorization

### ✅ Implemented
- Token-based authentication
- JWT tokens with expiration
- Password hashing (PBKDF2)
- Session management
- CSRF protection

### Configuration

```python
# settings.py
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
COOKIE_SECURE = True
COOKIE_HTTPONLY = True
```

## Input Validation

### ✅ Implemented
- Serializer validation
- Type checking
- Length validation
- Format validation
- SQL injection prevention (ORM)

## Security Headers

### Nginx Configuration
```nginx
# Prevent clickjacking
add_header X-Frame-Options "SAMEORIGIN" always;

# Prevent MIME type sniffing
add_header X-Content-Type-Options "nosniff" always;

# Enable XSS protection
add_header X-XSS-Protection "1; mode=block" always;

# Force HTTPS
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

# Referrer Policy
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

## Rate Limiting

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

## SSL/TLS Configuration

### Let's Encrypt Setup
```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --nginx -d yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

## Dependency Scanning

### Check for Vulnerabilities
```bash
# Safety
pip install safety
safety check

# Bandit (code security)
bandit -r apps/
```

## Regular Security Audits

### Checklist
- [ ] Update all dependencies monthly
- [ ] Run security scans (bandit, safety)
- [ ] Review access logs
- [ ] Test authentication/authorization
- [ ] Verify SSL certificates
- [ ] Check password policies
- [ ] Review API permissions

## Tools
- OWASP ZAP (penetration testing)
- Burp Suite (security testing)
- Nessus (vulnerability scanning)
