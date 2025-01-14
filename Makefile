MANAGE := poetry run

start:
	$(MANAGE) uvicorn  fast_python_api.main:app --reload


generate_requirements:
	poetry export --without-hashes -f requirements.txt -o requirements.txt
