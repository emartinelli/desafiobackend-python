.PHONY: run black isort db/upgrade test test/db

run:
	poetry run uvicorn main:app --reload

format:
	poetry run black .

isort:
	poetry run isort .

db/upgrade:
	alembic upgrade head

test/db:
	docker-compose up -d --no-recreate db

test: test/db
	poetry run pytest -v tests