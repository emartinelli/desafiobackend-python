.PHONY: run black

run:
	poetry run uvicorn main:app --reload

format:
	poetry run black .