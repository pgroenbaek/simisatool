#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"
VENV_DIR="$ROOT_DIR/.venv"

PYTHON="${PYTHON:-python3}"

cd "$ROOT_DIR"

echo "==> Creating virtual environment"
if [[ ! -x "$VENV_DIR/bin/python" ]]; then
    "$PYTHON" -m venv "$VENV_DIR"
fi

VENV_PYTHON="$VENV_DIR/bin/python"

echo "==> Installing dependencies"
"$VENV_PYTHON" -m pip install --upgrade pip
"$VENV_PYTHON" -m pip install -r "$ROOT_DIR/requirements.txt"
"$VENV_PYTHON" -m pip install nuitka

echo "==> Cleaning dist/"
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

echo "==> Building Nuitka executable"
"$VENV_PYTHON" -m nuitka \
    --onefile \
    --python-flag=-m \
    --output-dir="$DIST_DIR" \
    --output-filename=simisatool \
    "$ROOT_DIR/simisatool"

echo
echo "==> Build complete:"
ls -lh "$DIST_DIR"