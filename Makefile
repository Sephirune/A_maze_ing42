PYTHON      = python3
MAIN        = a_maze_ing.py
CONFIG      = config.txt
VENV        = .venv
PIP         = pip

.PHONY: install run debug lint lint-strict  venv clean

install: # Instalar dependencias
		$(PIP) install -r requirements.txt

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

lint: # Verificación del linting (estilo del código)
	flake8 .
	mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	flake8
	mypy . --strict

venv: # Crear entorno virtual
		python3 -m venv $(VENV)
		@echo "Activate with: source venv/bin/activate"

clean: # Limpiar los archivos de caché y artefacto
		find . -type f -name "*.pyc" -delete
		find . -type d -name "__pycache__" -delete
		find . -type d -name ".mypy_cache" -exec rm -rf {} +
		rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/