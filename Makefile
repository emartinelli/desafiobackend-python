.PHONY: run black isort db/upgrade

run:
	poetry run uvicorn main:app --reload

format:
	poetry run black .

isort:
	poetry run isort .

db/upgrade:
	alembic upgrade head