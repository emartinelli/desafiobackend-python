.PHONY: run/dev black isort db/upgrade test test/db

run/db:
	docker-compose up -d --no-recreate db

run/dev: run/db
	poetry run uvicorn main:app --reload

black:
	black --config ./pyproject.toml app tests

isort:
	isort --settings-path ./pyproject.toml app tests

format: black isort

db/upgrade:
	alembic upgrade head

test: run/db
	poetry run pytest -v tests