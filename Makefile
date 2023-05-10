.PHONY: run
run:
	uvicorn main:app --reload

.PHONY: run-prod
run-prod:
	uvicorn main:app --host 0.0.0.0

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: test
test: # Runs pytest
	pytest tests/test.py

.PHONY: lint
lint: # Lint code
	black --line-length 80 --skip-string-normalization .
	flake8 --ignore=E203,W503 --max-line-length=80 --exclude venv .
	mypy --ignore-missing-imports --exclude venv .

.PHONY: check
check: lint test