#!/usr/bin/env bash
set -e

# Check if uv is installed
if ! command -v uv >/dev/null 2>&1; then
  echo "uv not found. Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.cargo/bin:$PATH"
else
  echo "uv is already installed."
fi

# Sync project dependencies
echo "Running uv sync..."
uv sync

echo "Done."
