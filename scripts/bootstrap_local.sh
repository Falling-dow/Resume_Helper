#!/usr/bin/env bash
set -euo pipefail

echo "[1/6] Checking prerequisites..."
command -v python3 >/dev/null || { echo "python3 not found"; exit 1; }
command -v npm >/dev/null || { echo "npm not found"; exit 1; }

echo "[2/6] Preparing env files..."
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
  cp .env.example .env
  echo "- Created root .env from .env.example"
fi
if [ ! -f "backend/.env" ] && [ -f "backend/.env.example" ]; then
  cp backend/.env.example backend/.env
  echo "- Created backend/.env from backend/.env.example"
fi
if [ ! -f "frontend/.env" ] && [ -f "frontend/.env.example" ]; then
  cp frontend/.env.example frontend/.env
  echo "- Created frontend/.env from frontend/.env.example"
fi

echo "[3/6] Setting up Python venv + deps (backend)..."
pushd backend >/dev/null
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
if [ "${MINIMAL:-1}" = "1" ]; then
  echo "Installing minimal backend deps (fast to run)..."
  pip install \
    'fastapi>=0.110' \
    'uvicorn[standard]>=0.23' \
    'pydantic>=2.4' \
    'pydantic-settings>=2.0' \
    'email-validator>=2.0' \
    'python-multipart>=0.0.6' \
    'passlib[bcrypt]>=1.7' \
    'python-jose[cryptography]>=3.3' \
    'aiofiles>=23.1'
else
  echo "Installing full dev backend deps (may take longer)..."
  pip install -r requirements/dev.txt
fi
deactivate
popd >/dev/null

echo "[4/6] Installing Node dependencies (frontend)..."
pushd frontend >/dev/null
# Prefer install to avoid requiring a lockfile locally
npm install
popd >/dev/null

echo "[5/6] Smoke test: starting backend (background)"
(cd backend && . .venv/bin/activate && uvicorn app.main:app --host 127.0.0.1 --port 8000 & echo $! > ../.backend.pid)
sleep 2 || true

echo "[6/6] All set. Next steps:"
echo "- Backend: kill \`cat .backend.pid\` when done, or run: pkill -f 'uvicorn app.main:app'"
echo "- Frontend: cd frontend && npm run dev (opens http://localhost:5173)"
echo "- API health: curl http://localhost:8000/health"
