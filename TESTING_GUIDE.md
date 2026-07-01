# 🧪 Testing Guide

## Test Structure

```
apps/
├── users/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   └── test_serializers.py
├── products/
│   └── tests/
└── orders/
    └── tests/
```

## Running Tests

### All Tests
```bash
pytest
```

### Specific Test File
```bash
pytest apps/users/tests/test_models.py
```

### Specific Test Class
```bash
pytest apps/users/tests/test_models.py::UserModelTest
```

### With Coverage
```bash
pytest --cov=apps --cov-report=html
# Report saved to htmlcov/index.html
```

### With Markers
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run all except slow tests
pytest -m "not slow"
```

## Test Categories

### Unit Tests
- Test individual functions/methods
- No external dependencies
- Fast execution
- Markers: `@pytest.mark.unit`

### Integration Tests
- Test multiple components together
- May use database
- Slower execution
- Markers: `@pytest.mark.integration`

### Performance Tests
- Measure response times
- Load testing
- Markers: `@pytest.mark.slow`

### Security Tests
- Test authentication
- Test authorization
- Test input validation
- Markers: `@pytest.mark.security`

## Writing Tests

### Test Models

```python
import pytest
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestUserModel:
    def test_user_creation(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
```

### Test Views

```python
import pytest
from django.test import Client

@pytest.mark.django_db
class TestUserViews:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = Client()

    def test_user_list_view(self):
        response = self.client.get('/api/v1/users/')
        assert response.status_code == 200
```

## Coverage Goals

- Minimum: 80%
- Target: 90%
- Critical paths: 100%

## Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install
```
