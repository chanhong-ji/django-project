#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install

python manage.py collectstatic --no-input
python manage.py migrate
pip install --force-reinstall -U pip
pip install --force-reinstall -U setuptools