MANAGE := poetry run

install:
	poetry install

start:
	$(MANAGE) uvicorn  fast_python_api.main:app --reload

start_production:
	$(MANAGE) uvicorn fast_python_api.main:app --host 0.0.0.0 --port 8000


generate_requirements:
	poetry export --without-hashes -f requirements.txt -o requirements.txt

lint:
	$(MANAGE) flake8 fast_python_api

migrate:
	${MANAGE} alembic revision --autogenerate

migrate_up:
	${MANAGE} alembic upgrade head

build:
	make migrate
	make migrate_up

test:
	$(MANAGE) pytest -vvv

test-coverage:
	poetry run pytest --cov=./ --cov-report=xml

shell:
	$(MANAGE) ipython

dev:
	docker-compose -f docker-compose.dev.yml up --build

stop-dev:
	docker-compose -f docker-compose.dev.yml down

logs-dev:
	docker-compose -f docker-compose.dev.yml logs -f

build-prod:
	docker build --no-cache -t fast_python_api:latest .

prod:
	docker-compose -f docker-compose.prod.yml up -d

stop-prod:
	docker-compose -f docker-compose.prod.yml down

logs-prod:
	docker-compose -f docker-compose.prod.yml logs
