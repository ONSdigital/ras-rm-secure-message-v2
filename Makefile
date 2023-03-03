build:
	pipenv install --dev

start:
	pipenv run python run.py

lint:
	#pipenv check
	pipenv run isort .
	pipenv run black --line-length 120 .
	pipenv run flake8

lint-check:
	#pipenv check -i 51668
	pipenv run isort --check-only .
	pipenv run black --line-length 120 .
	pipenv run flake8