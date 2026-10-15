#!/usr/bin/env bash
# Simple verify script for StudyMate scaffold
# Checks for essential files and prints status table

echo "--- StudyMate Verify ---"

# Check Makefile exists
if [[ -f Makefile ]]; then echo "[OK] Makefile present"; else echo "[FAIL] Makefile missing"; fi

# Check .env.example
if [[ -f .env.example ]]; then echo "[OK] .env.example present"; else echo "[FAIL] .env.example missing"; fi

# Check backend main
if [[ -f backend/app/main.py ]]; then echo "[OK] backend/app/main.py present"; else echo "[FAIL] backend/app/main.py missing"; fi

# Check health router
if [[ -f backend/app/routers/health.py ]]; then echo "[OK] health router present"; else echo "[FAIL] health router missing"; fi

# Check python environment (venv)
if [[ -d .venv ]]; then echo "[OK] .venv directory exists"; else echo "[WARN] .venv not set up (run make setup)"; fi

# Check frontend placeholder (just check folder exists)
if [[ -d frontend ]]; then echo "[OK] frontend folder present"; else echo "[WARN] frontend folder missing"; fi

echo "--- End Verify ---"
