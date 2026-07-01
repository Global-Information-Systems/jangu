.PHONY: help install migrate test coverage run dev docker-up docker-down docker-build clean lint format security

help:
	@echo "Jangu Production Makefile"
	@echo "========================"
	@echo ""
	@echo "Available commands:"
	@echo "  make install          - Install dependencies"
	@echo "  make migrate          - Run database migrations"
	@echo "  make test             - Run test suite"
	@echo "  make coverage         - Run tests with coverage report"
	@echo "  make run              - Run development server"
	@echo "  make dev              - Run with hot reload"
	@echo "  make docker-build     - Build Docker images"
	@echo "  make docker-up        - Start Docker containers"
	@echo "  make docker-down      - Stop Docker containers"
	@echo "  make lint             - Run code linting (Flake8)"
	@echo "  make format           - Format code (Black, isort)"
	@echo "  make security         - Run security checks (Bandit)"
	@echo "  make clean            - Clean temporary files"
	@echo "  make prod-check       - Full production readiness check"

install:
	pip install -r requirements.txt

migrate:
	python manage.py migrate

test:
	pytest -v

coverage:
	pytest --cov=apps --cov-report=html --cov-report=term-missing

run:
	python manage.py runserver 0.0.0.0:8000

dev:
	python manage.py runserver --reload 0.0.0.0:8000

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d
	@echo "Services are up!"
	@echo "API: http://localhost:8000"
	@echo "Nginx: http://localhost"

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

lint:
	flake8 apps/ --max-line-length=100 --exclude=migrations
	pylint apps/ --disable=all --enable=E,F

format:
	black apps/ --line-length=100
	isort apps/ --profile black

security:
	bandit -r apps/ -ll

prod-check: lint coverage security
	@echo "✅ All production checks passed!"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info
