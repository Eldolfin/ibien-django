#!/usr/bin/bash
export DJANGO_SETTINGS_MODULE=my_django_project.settings-dev
source venv/bin/activate
python manage.py "$@"
