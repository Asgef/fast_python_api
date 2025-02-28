MANAGE := poetry run

install:
	poetry install

start:
	$(MANAGE) uvicorn  fast_python_api.main:app --reload

start_production:
	$(MANAGE) uvicorn  fast_python_api.main:app


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