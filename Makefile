# Makefile scaffold for StudyMate project

# Variables
PYTHON ?= python
PIP ?= pip
ENV_FILE ?= .env

# Targets
.PHONY: setup dev seed verify test eval export clean

setup:
	@echo "Setting up virtual environment and installing dependencies..."
	$(PYTHON) -m venv .venv
	.venv\\Scripts\\activate && $(PIP) install -r requirements.txt

dev:
	@echo "Running backend and frontend in development mode..."
	# Backend dev server
	cd backend && .venv\\Scripts\\activate && uvicorn app.main:app --reload &
	# Frontend dev server
	cd frontend && npm install && npm run dev

seed:
	@echo "Seeding demo data without external API calls..."
	# Placeholder for seed script
	bash scripts/seed.sh

verify:
	@echo "Verifying project scaffold..."
	bash scripts/verify.sh

test:
	@echo "Running tests..."
	cd backend && .venv\\Scripts\\activate && pytest

eval:
	@echo "Running evaluation pipelines..."
	# Placeholder for eval scripts
	python eval/run_all.py

export:
	@echo "Exporting project for deployment..."
	# Placeholder for export script
	bash scripts/export.sh

clean:
	@echo "Cleaning build artifacts..."
	rm -rf .venv build dist
