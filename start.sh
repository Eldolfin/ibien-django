#!/usr/bin/bash
source venv/bin/activate
tmux new-session -s "web" python manage.py runserver
