PYTHON      = $(VENV)/bin/python
PIP         = $(VENV)/bin/pip
MAIN        = a_maze_ing.py
CONFIG      = config.txt
VENV        = .venv

.PHONY: install run debug lint lint-strict venv clean

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install mlx
	# or: $(PIP) install -r requirements.txt

run: venv
	$(PYTHON) $(MAIN) $(CONFIG)

debug: venv
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

lint: venv
	$(PIP) install flake8 mypy
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict: venv
	$(PIP) install flake8 mypy
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --strict

venv:
	python3 -m venv $(VENV)
	@echo "Activate with: source $(VENV)/bin/activate"

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/ $(VENV)