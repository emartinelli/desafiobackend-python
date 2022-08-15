.PHONY: run/dev black isort db/upgrade test test/db

run/dev:
	poetry run uvicorn main:app --reload

black:
	black --config ./pyproject.toml app tests

isort:
	isort --settings-path ./pyproject.toml --recursive app tests

format: black isort

db/upgrade:
	alembic upgrade head

test/db:
	docker-compose up -d --no-recreate db

test: test/db
	poetry run pytest -v tests