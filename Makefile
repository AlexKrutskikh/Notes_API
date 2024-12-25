# variables
PYTHON_SRC := apps

# installing dependencies
.PHONY: deps
deps:
	pip install --progress-bar off --upgrade pip
	pip install --progress-bar off -r requirements-dev.txt
	pip install --progress-bar off -r requirements.txt

# code check by linters
.PHONY: lint
lint:
	black --check $(PYTHON_SRC)
	isort --check $(PYTHON_SRC)
	flake8 $(PYTHON_SRC)

# code formatting
.PHONY: format
format:
	black $(PYTHON_SRC)
	isort $(PYTHON_SRC)
