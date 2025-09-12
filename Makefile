SHELL := /bin/bash

PROJECT := resume-helper
COMPOSE := docker-compose

.PHONY: setup dev stop logs test build deploy migrate createsuperuser fmt lint

setup:
	bash scripts/bootstrap_local.sh

dev:
	$(COMPOSE) up -d --build

stop:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f --tail=200

test:
	$(COMPOSE) exec -T backend pytest -q || true
	$(COMPOSE) exec -T frontend npm test --silent || true

build:
	$(COMPOSE) build

deploy:
	@echo "Deploy is handled by GitHub Actions (see .github/workflows)."

migrate:
	$(COMPOSE) exec -T backend alembic upgrade head || true

createsuperuser:
	$(COMPOSE) exec -T backend python -c "print('Implement createsuperuser script in backend/scripts')"

fmt:
	$(COMPOSE) exec -T backend black app || true
	$(COMPOSE) exec -T backend isort app || true

lint:
	$(COMPOSE) exec -T backend flake8 app || true
	$(COMPOSE) exec -T backend mypy app || true
