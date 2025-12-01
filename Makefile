VENVDIR = venv

setup:
	( \
		python3 -m venv $(VENVDIR); \
		. $(VENVDIR)/bin/activate; \
		pip install -r requirements.txt; \
		pip install -r requirements-dev.txt; \
	)

server:
	( \
		. $(VENVDIR)/bin/activate; \
		python3 src/main.py; \
	)

inspector:
	( \
		. $(VENVDIR)/bin/activate; \
		npm start; \
	)

lint:
	( \
		. $(VENVDIR)/bin/activate; \
		ruff check src/; \
	)

fix:
	( \
		. $(VENVDIR)/bin/activate; \
		ruff check --fix --select I; \
		ruff format src/; \
	)

docker:
	mkdir -p .ollama/ollama/ .ollama/open-webui/;
	docker compose up;

.PHONY: lint fix server setup ollama
