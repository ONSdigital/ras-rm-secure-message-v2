.PHONY: build start

build:
	pipenv install --dev

start:
	pipenv run python run.py

lint:
	pipenv run isort .
	pipenv run black --line-length 120 .
	pipenv run flake8
	pipenv run mypy secure_message_v2

lint-check:
	pipenv run isort --check-only .
	pipenv run black --line-length 120 .
	pipenv run flake8
	pipenv run mypy secure_message_v2

test: lint-check
	pipenv run pytest --cov secure_message_v2 --cov-report term-missing --cov-report html --cov-fail-under=100

build-docker:
	docker build .

build-kubernetes:
	docker build -f _infra/docker/Dockerfile .