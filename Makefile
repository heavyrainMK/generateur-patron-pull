# ====== Générateur de Patrons de Tricot - Makefile ======
# Cibles: make install, make dev, make stop, make test, make clean, make help

# --- Racine & venv ---
ROOT_DIR := $(CURDIR)
VENV_DIR := venv
VENV_BIN := $(VENV_DIR)/bin
PY := $(VENV_BIN)/python
PIP := $(VENV_BIN)/pip

# --- Dossiers ---
NODE_DIR := node-backend
PY_DIR := backend

# --- Ports ---
PORT_NODE ?= 3000
PORT_FLASK ?= 10000

# --- PID en chemins absolus ---
PID_NODE := $(ROOT_DIR)/.node.pid
PID_FLASK := $(ROOT_DIR)/.flask.pid

.PHONY: help install install-node install-py dev start-flask start-node stop test test-py clean

help:
	@echo "Cibles:"
	@echo "  make install  - Installe Node + Python (venv)"
	@echo "  make dev      - Démarre Flask (port $(PORT_FLASK)) + Node (port $(PORT_NODE))"
	@echo "  make stop     - Stoppe les deux serveurs"
	@echo "  make test     - Lance les tests Python"
	@echo "  make clean    - Nettoie venv, node_modules, PID, caches"
	@echo ""
	@echo "Variables: PORT_NODE=$(PORT_NODE), PORT_FLASK=$(PORT_FLASK)"

# ====== INSTALL ======
install: install-node install-py
	@echo "✅ Installation terminée."

install-node:
	@echo "📦 Installation deps Node…"
	cd $(NODE_DIR) && npm install

install-py:
	@echo "🐍 Préparation venv + deps Python…"
	python3 -m venv $(VENV_DIR) 2>/dev/null || python -m venv $(VENV_DIR)
	$(PIP) -q install --upgrade pip
	$(PIP) install -r $(PY_DIR)/requirements.txt

# ====== DEV (Node + Flask en parallèle) ======
dev: install start-flask start-node
	@echo "🌐 Flask: http://127.0.0.1:$(PORT_FLASK)"
	@echo "🟢 Node : http://127.0.0.1:$(PORT_NODE)"
	@echo "👉 Ctrl+C pour arrêter la session courante, ou 'make stop' pour tuer les process en arrière-plan."
	@wait

start-flask:
	@echo "🚀 Démarrage Flask (port $(PORT_FLASK))…"
	@if lsof -tiTCP:$(PORT_FLASK) -sTCP:LISTEN >/dev/null 2>&1; then \
		echo "❌ Port $(PORT_FLASK) déjà utilisé. Lance 'make stop' ou libère le port."; \
		exit 1; \
	fi
	@sh -c 'cd $(PY_DIR) && \
		FLASK_APP=app.py exec ../$(VENV_BIN)/python -m flask run \
		--host=127.0.0.1 --port=$(PORT_FLASK) --no-reload --no-debugger' \
		> /dev/stdout 2>&1 & echo $$! > "$(PID_FLASK)"

start-node:
	@echo "🚀 Démarrage Node (port $(PORT_NODE))…"
	@if lsof -tiTCP:$(PORT_NODE) -sTCP:LISTEN >/dev/null 2>&1; then \
		echo "❌ Port $(PORT_NODE) déjà utilisé. Lance 'make stop' ou libère le port."; \
		exit 1; \
	fi
	@sh -c 'cd $(NODE_DIR) && PORT=$(PORT_NODE) exec node server.js' \
		> /dev/stdout 2>&1 & echo $$! > "$(PID_NODE)"

# ====== STOP ======
stop:
	@echo "🛑 Arrêt des services…"
	-@if [ -f "$(PID_FLASK)" ]; then \
		PID=$$(cat "$(PID_FLASK)"); \
		kill $$PID 2>/dev/null || true; \
		sleep 0.5; \
		if ps -p $$PID >/dev/null 2>&1; then kill -9 $$PID 2>/dev/null || true; fi; \
		rm -f "$(PID_FLASK)"; \
		echo "  ✔ Flask stoppé"; \
	else \
		echo "  (Flask déjà arrêté)"; \
	fi
	-@if [ -f "$(PID_NODE)" ]; then \
		PID=$$(cat "$(PID_NODE)"); \
		kill $$PID 2>/dev/null || true; \
		sleep 0.5; \
		if ps -p $$PID >/dev/null 2>&1; then kill -9 $$PID 2>/dev/null || true; fi; \
		rm -f "$(PID_NODE)"; \
		echo "  ✔ Node stoppé"; \
	else \
		echo "  (Node déjà arrêté)"; \
	fi
	-@command -v fuser >/dev/null 2>&1 && fuser -k -n tcp $(PORT_FLASK) 2>/dev/null || true
	-@command -v lsof  >/dev/null 2>&1 && lsof -tiTCP:$(PORT_FLASK) -sTCP:LISTEN | xargs -r kill -9 2>/dev/null || true
	-@command -v fuser >/dev/null 2>&1 && fuser -k -n tcp $(PORT_NODE)  2>/dev/null || true
	-@command -v lsof  >/dev/null 2>&1 && lsof -tiTCP:$(PORT_NODE)  -sTCP:LISTEN | xargs -r kill -9 2>/dev/null || true
	@stty sane || true

# ====== TESTS ======
test: test-py

test-py:
	@echo "🧪 Tests Python…"
	@PYTHONPATH=./$(PY_DIR) $(PY) -m unittest discover -s $(PY_DIR) -p 'tests_*.py' -v -b || true

# ====== CLEAN ======
clean:
	@echo "🧹 Nettoyage…"
	-rm -rf $(VENV_DIR)
	-rm -rf $(NODE_DIR)/node_modules
	-rm -f "$(PID_NODE)" "$(PID_FLASK)"
	-find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	-find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Clean OK"