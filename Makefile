MANAGE := poetry run

install:
	$(MANAGE) install

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

test:
	$(MANAGE) pytest -vvv

test-coverage:
	poetry run pytest --cov=./ --cov-report=xml