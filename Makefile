# variables
PYTHON_SRC := apps
VENV := .\.venv\Scripts

# installing dependencies
.PHONY: deps
deps:
	pip install --progress-bar off --upgrade pip
	pip install --progress-bar off -r requirements-dev.txt
	pip install --progress-bar off -r requirements.txt

# code check by linters
.PHONY: lint
lint:
	$(VENV)\black --check $(PYTHON_SRC)
	$(VENV)\isort --check $(PYTHON_SRC)
	$(VENV)\flake8 $(PYTHON_SRC)

# code formatting
.PHONY: format
format:
	$(VENV)\black $(PYTHON_SRC)
	$(VENV)\isort $(PYTHON_SRC)
