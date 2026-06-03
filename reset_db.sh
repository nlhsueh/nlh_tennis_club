#!/bin/zsh
set -e

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"

PYTHON=python3
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  PYTHON=python
fi

if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "Error: Python is not found. Please install Python or activate your virtual environment."
  exit 1
fi

rm -f db.sqlite3 db.sqlite3-journal

"$PYTHON" manage.py migrate
"$PYTHON" manage.py loaddata initial_data.json

echo "Reset complete. Database has been rebuilt and seeded."
