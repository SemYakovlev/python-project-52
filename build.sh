#!/usr/bin/env bash
set -o errexit

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

uv pip install --system -r pyproject.toml

python manage.py collectstatic --no-input
python manage.py migrate